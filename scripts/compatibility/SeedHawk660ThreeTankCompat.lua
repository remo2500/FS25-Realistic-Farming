-- Seed Hawk 660 three-tank Realistic Seeder/custom seed compatibility bridge.
-- V3R2 seed-acceptance hotfix.
--
-- Base SEEDS/FERTILIZER remain explicit in vehicle XML so the cart stays
-- fillable even if this compatibility bridge or an external category extension
-- is unavailable. Lua expands the supported set; it is not sole base authority.

SeedHawk660ThreeTankCompat = {}
SeedHawk660ThreeTankCompat.scanTimer = 0
SeedHawk660ThreeTankCompat.scanInterval = 750

local function isTargetSeedHawk660(vehicle)
    if vehicle == nil or vehicle.spec_fillUnit == nil or vehicle.spec_fillUnit.fillUnits == nil then
        return false
    end

    if #vehicle.spec_fillUnit.fillUnits < 3 then
        return false
    end

    local configName = string.lower(vehicle.configFileName or "")
    return string.find(configName, "seedhawk660aircart.xml", 1, true) ~= nil
end

-- GIANTS manager helpers return array-style lists of fillType indices, while
-- FillUnit.supportedFillTypes is a set keyed by fillTypeIndex. Accept both forms.
local function addFillTypeCollection(dst, src)
    if src == nil then return end

    for key, value in pairs(src) do
        if type(value) == "number" then
            dst[value] = true
        elseif value == true and type(key) == "number" then
            dst[key] = true
        end
    end
end

local function addNamedFillType(dst, name)
    if g_fillTypeManager == nil or g_fillTypeManager.nameToIndex == nil then
        return
    end

    local fillTypeIndex = g_fillTypeManager.nameToIndex[string.upper(name)]
    if fillTypeIndex ~= nil then
        dst[fillTypeIndex] = true
    end
end

local function getDesiredFillTypes(vehicle)
    local desired = {}
    local units = vehicle.spec_fillUnit.fillUnits

    -- Preserve every type already supported by any of the three tanks.
    -- V3R2 XML guarantees generic SEEDS and FERTILIZER are present before Lua runs.
    for i = 1, 3 do
        local unit = units[i]
        if unit ~= nil then
            addFillTypeCollection(desired, unit.supportedFillTypes)
        end
    end

    if g_fillTypeManager ~= nil then
        -- Direct fill-type lookup for the two generic base inputs.
        if g_fillTypeManager.getFillTypesByNames ~= nil then
            addFillTypeCollection(desired, g_fillTypeManager:getFillTypesByNames("seeds fertilizer"))
        else
            addNamedFillType(desired, "SEEDS")
            addNamedFillType(desired, "FERTILIZER")
        end

        -- Include custom dry fertilizer products registered in the native
        -- FERTILIZER category. This is supplemental, not base input authority.
        if g_fillTypeManager.getFillTypesByCategoryNames ~= nil then
            addFillTypeCollection(desired, g_fillTypeManager:getFillTypesByCategoryNames("fertilizer"))
        end

        -- Realistic Seeder / multifruit fallback for standalone crop seed types.
        if g_fillTypeManager.nameToIndex ~= nil then
            for name, fillTypeIndex in pairs(g_fillTypeManager.nameToIndex) do
                local upperName = string.upper(tostring(name))
                if upperName ~= "SEEDS" and string.sub(upperName, -4) == "SEED" then
                    desired[fillTypeIndex] = true
                end
            end
        end
    end

    return desired
end

local function synchronizeVehicle(vehicle)
    local units = vehicle.spec_fillUnit.fillUnits
    local desired = getDesiredFillTypes(vehicle)
    local changed = false
    local count = 0

    for _ in pairs(desired) do
        count = count + 1
    end

    for i = 1, 3 do
        local unit = units[i]
        if unit ~= nil then
            unit.supportedFillTypes = unit.supportedFillTypes or {}
            for fillTypeIndex, enabled in pairs(desired) do
                if enabled and not unit.supportedFillTypes[fillTypeIndex] then
                    unit.supportedFillTypes[fillTypeIndex] = true
                    changed = true
                end
            end
        end
    end

    if changed then
        local root = vehicle.rootVehicle or vehicle
        if root ~= nil and root.raiseStateChange ~= nil and VehicleStateChange ~= nil then
            root:raiseStateChange(VehicleStateChange.FILLTYPE_CHANGE)
        end

        Logging.info("[SeedHawk660-3Tank RS V3R2] Synchronized Tanks 1-3 to %d supported fill types and refreshed source caches", count)
    elseif not vehicle.seedHawk660ThreeTankCompatLogged then
        Logging.info("[SeedHawk660-3Tank RS V3R2] Tanks 1-3 already synchronized (%d supported fill types)", count)
    end

    vehicle.seedHawk660ThreeTankCompatLogged = true
end

function SeedHawk660ThreeTankCompat:update(dt)
    self.scanTimer = self.scanTimer + dt
    if self.scanTimer < self.scanInterval then
        return
    end
    self.scanTimer = 0

    if g_currentMission == nil or g_currentMission.vehicles == nil then
        return
    end

    for _, vehicle in pairs(g_currentMission.vehicles) do
        if isTargetSeedHawk660(vehicle) then
            synchronizeVehicle(vehicle)
        end
    end
end

function SeedHawk660ThreeTankCompat:loadMap(mapNode, mapFilename)
    self.scanTimer = self.scanInterval
end

function SeedHawk660ThreeTankCompat:deleteMap()
    self.scanTimer = 0
end

function SeedHawk660ThreeTankCompat:draw() end
function SeedHawk660ThreeTankCompat:keyEvent(unicode, sym, modifier, isDown) end
function SeedHawk660ThreeTankCompat:mouseEvent(posX, posY, isDown, isUp, button) end

addModEventListener(SeedHawk660ThreeTankCompat)
