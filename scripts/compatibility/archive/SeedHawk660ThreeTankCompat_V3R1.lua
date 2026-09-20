-- Seed Hawk 660 three-tank Realistic Seeder/custom seed compatibility bridge.
-- Keeps Tanks 1-3 synchronized even when an external seeding mod patches only one donor unit.

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

local function addSet(dst, src)
    if src == nil then return end
    for fillTypeIndex, enabled in pairs(src) do
        if enabled then
            dst[fillTypeIndex] = true
        end
    end
end

local function getDesiredFillTypes(vehicle)
    local desired = {}
    local units = vehicle.spec_fillUnit.fillUnits

    -- Preserve anything another mod has already added to any one of the three tanks.
    for i = 1, 3 do
        local unit = units[i]
        if unit ~= nil then
            addSet(desired, unit.supportedFillTypes)
        end
    end

    if g_fillTypeManager ~= nil then
        -- Include the normal and mod-extended seed/fertilizer categories.
        if g_fillTypeManager.getFillTypesByCategoryNames ~= nil then
            addSet(desired, g_fillTypeManager:getFillTypesByCategoryNames("seeds fertilizer"))
        end

        -- Compatibility fallback for Realistic Seeder/multifruit seed products that
        -- are not added to the normal seeds category. Accept only names that actually
        -- end in SEED (for example GREENBEAN_SEED or WHEATSEED), rather than any name
        -- containing the letters SEED somewhere in the middle.
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
        -- SowingMachine/Sprayer rebuild attached source lists from this state change.
        local root = vehicle.rootVehicle or vehicle
        if root ~= nil and root.raiseStateChange ~= nil and VehicleStateChange ~= nil then
            root:raiseStateChange(VehicleStateChange.FILLTYPE_CHANGE)
        end

        Logging.info("[SeedHawk660-3Tank RS V3] Synchronized Tanks 1-3 to %d supported fill types and refreshed source caches", count)
    elseif not vehicle.seedHawk660ThreeTankCompatLogged then
        Logging.info("[SeedHawk660-3Tank RS V3] Tanks 1-3 already synchronized (%d supported fill types)", count)
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
