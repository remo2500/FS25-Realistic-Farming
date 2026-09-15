-- Bourgault 7950 V6 four-tank Realistic Seeder / custom-input compatibility bridge.
-- Goal: Tanks 1-4 expose the same seed/fertilizer product set even when another mod
-- patches only the donor cart's former seed/fertilizer units after vehicle XML load.

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
        if enabled then dst[fillTypeIndex] = true end
    end
end

local function getDesiredFillTypes(vehicle)
    local desired = {}
    local units = vehicle.spec_fillUnit.fillUnits

    -- Preserve anything already registered on any compartment. This captures late patches
    -- from Realistic Seeder and other input mods without hard-coding their load order.
    for i = 1, 4 do
        local unit = units[i]
        if unit ~= nil then addSet(desired, unit.supportedFillTypes) end
    end

    if g_fillTypeManager ~= nil then
        -- Standard and mod-extended seed/fertilizer categories.
        if g_fillTypeManager.getFillTypesByCategoryNames ~= nil then
            addSet(desired, g_fillTypeManager:getFillTypesByCategoryNames("seeds fertilizer"))
        end

        -- Realistic Seeder and multifruit packs normally expose crop-specific products with
        -- SEED in the internal fill-type name (e.g. GREENBEAN_SEED). Include those explicitly
        -- so map-specific seed products are not lost if they were not added to the base category.
        if g_fillTypeManager.nameToIndex ~= nil then
            for name, fillTypeIndex in pairs(g_fillTypeManager.nameToIndex) do
                if string.find(string.upper(tostring(name)), "SEED", 1, true) ~= nil then
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

    for _ in pairs(desired) do count = count + 1 end

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
        -- SowingMachine and Sprayer rebuild their attached fill-type source lists on this state
        -- change. Without it, a late compatibility patch could leave Tanks 1/2 invisible until
        -- another unrelated fill-type or attachment event occurred.
        local root = vehicle.rootVehicle or vehicle
        if root ~= nil and root.raiseStateChange ~= nil and VehicleStateChange ~= nil then
            root:raiseStateChange(VehicleStateChange.FILLTYPE_CHANGE)
        end
        Logging.info("[Bourgault7950-4Tank V6] Updated Tanks 1-4 to %d supported fill types and refreshed source caches", count)
    elseif not vehicle.bourgault7950FourTankCompatLogged then
        Logging.info("[Bourgault7950-4Tank V6] Tanks 1-4 already synchronized (%d supported fill types)", count)
    end

    vehicle.bourgault7950FourTankCompatLogged = true
end

function Bourgault7950FourTankCompat:update(dt)
    self.scanTimer = self.scanTimer + dt
    if self.scanTimer < self.scanInterval then return end
    self.scanTimer = 0

    if g_currentMission == nil or g_currentMission.vehicles == nil then return end
    for _, vehicle in pairs(g_currentMission.vehicles) do
        if isTarget7950(vehicle) then synchronizeVehicle(vehicle) end
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
