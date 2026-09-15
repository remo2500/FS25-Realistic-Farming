-- Bourgault 7950 V7 four-tank Realistic Seeder / custom-input compatibility bridge.
-- Goal: Tanks 1-4 expose the same approved seed/fertilizer product set without
-- propagating arbitrary products that another mod may have added to only one tank.

Bourgault7950FourTankCompat = {}
Bourgault7950FourTankCompat.scanTimer = 0
Bourgault7950FourTankCompat.scanInterval = 750

local function isTarget7950(vehicle)
    if vehicle == nil or vehicle.spec_fillUnit == nil or vehicle.spec_fillUnit.fillUnits == nil then
        return false
    end
    if #vehicle.spec_fillUnit.fillUnits < 4 then
        return false
    end
    return string.find(vehicle.configFileName or "", "Series_7950B.xml", 1, true) ~= nil
end

local function addSet(dst, src)
    if src == nil then return end
    for fillTypeIndex, enabled in pairs(src) do
        if enabled then
            dst[fillTypeIndex] = true
        end
    end
end

local function isApprovedCustomSeedName(name)
    local upperName = string.upper(tostring(name or ""))

    -- Generic SEEDS is already supplied by the seeds category. The suffix fallback is
    -- deliberately narrower than V6's broad substring search, so names such as
    -- OILSEEDRADISH are not automatically treated as separate seed-input products.
    return upperName ~= "SEEDS" and string.sub(upperName, -4) == "SEED"
end

local function getDesiredFillTypes()
    local desired = {}

    if g_fillTypeManager ~= nil then
        -- Primary authority: normal categories plus any products that other mods correctly
        -- append to those categories. This includes mod-extended dry fertilizer products.
        if g_fillTypeManager.getFillTypesByCategoryNames ~= nil then
            addSet(desired, g_fillTypeManager:getFillTypesByCategoryNames("seeds fertilizer"))
        end

        -- Fallback for crop-specific Realistic Seeder / multifruit products that register as
        -- standalone fill types rather than joining the normal seeds category. This remains
        -- heuristic until the installed Realistic Seeder product registry is captured in game.
        if g_fillTypeManager.nameToIndex ~= nil then
            for name, fillTypeIndex in pairs(g_fillTypeManager.nameToIndex) do
                if isApprovedCustomSeedName(name) then
                    desired[fillTypeIndex] = true
                end
            end
        end
    end

    return desired
end

local function synchronizeVehicle(vehicle)
    local units = vehicle.spec_fillUnit.fillUnits
    local desired = getDesiredFillTypes()
    local changed = false
    local count = 0

    for _ in pairs(desired) do
        count = count + 1
    end

    for i = 1, 4 do
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
        -- SowingMachine and Sprayer rebuild attached fill-source lists on this state change.
        -- Without it, a late compatibility addition can remain invisible to the attached tool.
        local root = vehicle.rootVehicle or vehicle
        if root ~= nil and root.raiseStateChange ~= nil and VehicleStateChange ~= nil then
            root:raiseStateChange(VehicleStateChange.FILLTYPE_CHANGE)
        end

        Logging.info("[Bourgault7950-4Tank V7] Updated Tanks 1-4 to %d approved supported fill types and refreshed source caches", count)
    elseif not vehicle.bourgault7950FourTankCompatLogged then
        Logging.info("[Bourgault7950-4Tank V7] Tanks 1-4 already synchronized (%d approved supported fill types)", count)
    end

    vehicle.bourgault7950FourTankCompatLogged = true
end

function Bourgault7950FourTankCompat:update(dt)
    self.scanTimer = self.scanTimer + dt
    if self.scanTimer < self.scanInterval then
        return
    end
    self.scanTimer = 0

    if g_currentMission == nil or g_currentMission.vehicles == nil then
        return
    end

    for _, vehicle in pairs(g_currentMission.vehicles) do
        if isTarget7950(vehicle) then
            synchronizeVehicle(vehicle)
        end
    end
end

function Bourgault7950FourTankCompat:loadMap(mapNode, mapFilename)
    self.scanTimer = self.scanInterval
end

function Bourgault7950FourTankCompat:deleteMap()
    self.scanTimer = 0
end

function Bourgault7950FourTankCompat:draw() end
function Bourgault7950FourTankCompat:keyEvent(unicode, sym, modifier, isDown) end
function Bourgault7950FourTankCompat:mouseEvent(posX, posY, isDown, isUp, button) end

addModEventListener(Bourgault7950FourTankCompat)
