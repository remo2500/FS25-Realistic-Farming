#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, hashlib, os, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ACTIVE='-1.89549 2.74644 4.33058'
PARKED='-1.89549 12.74644 4.33058'
EXPECTED_SOURCE_SHA256='30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a'
DEFAULT_OUTPUT='FS25_Bourgault_3320_4Tank_V7_Engineering.zip'

TANK1_ANGLES=(105.164095,-59.356622,-145.314298,21.0)
TANK2_ANGLES=(100.0,-50.0,-135.0,21.0)
TANK3_ANGLES=(90.0,-33.0,-135.0,21.0)
TANK4_ANGLES=(83.122517,-27.956513,-124.148860,19.395254)
TRANSPORT_ANGLES=(0.0,0.0,0.0,0.0)

VOLUME_SPECS={
 'fillVolumeTank1':('0.028885 2.65800 2.121000','1.50 1.44 1.28'),
 'fillVolumeTank2':('0.028885 2.65800 0.721000','1.50 1.44 1.28'),
 'fillVolumeTank3':('0.028885 2.65800 -0.678000','1.50 1.44 1.20'),
 'fillVolumeTank4':('0.028885 2.65800 -2.129500','1.15 1.44 1.38'),
 'fillVolumeTank4Flex':('0.028885 2.65800 -3.606000','1.15 1.44 1.45'),
}
Z_TARGETS=[2.121,0.721,-0.678,-1.792]

def fmt(v:float)->str:
    if abs(v)<5e-8: v=0.0
    s=f'{v:.6f}'.rstrip('0').rstrip('.')
    return s if s else '0'

def vecrot(axis:str, val:float)->str:
    if axis=='y': return f'0 {fmt(val)} 0'
    if axis=='x': return f'{fmt(val)} 0 0'
    raise ValueError(axis)

def parse_xml(data:bytes)->ET.Element:
    return ET.fromstring(data)

def xml_bytes(root:ET.Element)->bytes:
    ET.indent(root, space='    ')
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def find_named(root:ET.Element,name:str):
    for e in root.iter():
        if e.get('name')==name:
            return e
    return None

def max_node_id(root):
    vals=[]
    for e in root.iter():
        n=e.get('nodeId')
        if n and n.isdigit(): vals.append(int(n))
    return max(vals) if vals else 0

def patch_i3d(data:bytes)->tuple[bytes,dict[str,str]]:
    root=parse_xml(data)
    # Volume transforms; reuse V3's unused Flex Tank 4 placeholder.
    flex=find_named(root,'fillVolumeFlexTank4_UNUSED')
    if flex is None:
        raise RuntimeError('fillVolumeFlexTank4_UNUSED not found in V3 donor')
    flex.set('name','fillVolumeTank4Flex')
    flex.attrib.pop('visibility',None)
    for name,(translation,scale) in VOLUME_SPECS.items():
        node=find_named(root,name)
        if node is None: raise RuntimeError(f'{name} not found')
        node.set('translation',translation); node.set('scale',scale)

    # The original four load/unload TransformGroups occupy 0|0|4|2..5.
    scene=root.find('Scene')
    if scene is None: raise RuntimeError('Scene missing')
    fill_parent=list(list(list(scene)[0])[0])[4]
    if fill_parent.get('name')!='fillUnit':
        raise RuntimeError('unexpected fillUnit scene path')
    children=list(fill_parent)
    if len(children)<9: raise RuntimeError('unexpected fillUnit child count')
    for i,z in enumerate(Z_TARGETS, start=1):
        node=children[i+1]  # indices 2..5
        node.tag='TransformGroup'
        node.attrib.clear()
        node.set('name',f'loadInfoTank{i}')
        node.set('translation',f'0 3.68986 {fmt(z)}')
        # preserve old donor node IDs for these four transforms
        node.set('nodeId',str(187+i+1))  # 189..192

    # Append four unload-info transforms with new node IDs.
    next_id=max_node_id(root)+1
    for i,z in enumerate(Z_TARGETS, start=1):
        node=ET.Element('TransformGroup',{
            'name':f'unloadInfoTank{i}',
            'translation':f'0 3.68986 {fmt(z)}',
            'nodeId':str(next_id),
        })
        next_id+=1
        fill_parent.append(node)

    # Return mapping paths after append. Existing first nine children stay stable.
    mapping={
        'fillVolumeTank4':'0>0|4|0',
        'fillVolumeTank1':'0>0|4|1',
        'loadInfoTank1':'0>0|4|2',
        'loadInfoTank2':'0>0|4|3',
        'loadInfoTank3':'0>0|4|4',
        'loadInfoTank4':'0>0|4|5',
        'fillVolumeTank4Flex':'0>0|4|6',
        'fillVolumeTank3':'0>0|4|7',
        'fillVolumeTank2':'0>0|4|8',
        'unloadInfoTank1':'0>0|4|9',
        'unloadInfoTank2':'0>0|4|10',
        'unloadInfoTank3':'0>0|4|11',
        'unloadInfoTank4':'0>0|4|12',
    }
    return xml_bytes(root),mapping

def add_part(anim, node, start, end, **attrs):
    a={'node':node,'startTime':fmt(start),'endTime':fmt(end)}
    a.update(attrs)
    return ET.Element('part',a)

def patch_vehicle(data:bytes,mapping:dict[str,str])->bytes:
    root=parse_xml(data)
    units=root.findall('./fillUnit/fillUnitConfigurations/fillUnitConfiguration/fillUnits/fillUnit')
    caps=['9691','1938','4228','17618']
    roots=['exactFillRootNodeTank1','exactFillRootNodeTank2','exactFillRootNodeTank3','exactFillRootNodeTank4']
    if len(units)!=4: raise RuntimeError(f'expected 4 fill units, found {len(units)}')
    for unit,cap,root_name in zip(units,caps,roots):
        unit.attrib.pop('fillTypes',None)
        unit.set('fillTypeCategories','seeds fertilizer')
        unit.set('capacity',cap)
        exact=unit.find('exactFillRootNode')
        if exact is None: exact=ET.SubElement(unit,'exactFillRootNode')
        exact.set('node',root_name)

    volumes=root.find('./fillVolume/fillVolumeConfigurations/fillVolumeConfiguration/volumes')
    if volumes is None: raise RuntimeError('volumes missing')
    volumes.clear()
    for i in range(1,4):
        ET.SubElement(volumes,'volume',{
            'node':f'fillVolumeTank{i}','fillUnitIndex':str(i),'maxDelta':'0.05',
            'maxAllowedHeapAngle':'12','retessellateTop':'true'})
    ET.SubElement(volumes,'volume',{
        'node':'fillVolumeTank4','fillUnitIndex':'4','fillUnitFactor':'0.82','useFullCapacity':'false',
        'maxDelta':'0.05','maxAllowedHeapAngle':'12','retessellateTop':'true'})
    ET.SubElement(volumes,'volume',{
        'node':'fillVolumeTank4Flex','fillUnitIndex':'4','fillUnitFactor':'0.18','useFullCapacity':'false',
        'maxDelta':'0.05','maxAllowedHeapAngle':'12','retessellateTop':'true'})

    unloads=root.find('./fillVolume/unloadInfos'); loads=root.find('./fillVolume/loadInfos')
    if unloads is None or loads is None: raise RuntimeError('load/unload infos missing')
    unloads.clear(); loads.clear()
    for i in range(1,5):
        ui=ET.SubElement(unloads,'unloadInfo'); ET.SubElement(ui,'node',{'node':f'unloadInfoTank{i}','width':'1.4','length':'0.1'})
        li=ET.SubElement(loads,'loadInfo'); ET.SubElement(li,'node',{'node':f'loadInfoTank{i}','width':'1.4','length':'0.1'})

    sprayer=root.find('./sprayer')
    if sprayer is None: raise RuntimeError('sprayer missing')
    sprayer.set('fillUnitIndex','1'); sprayer.set('unloadInfoIndex','1'); sprayer.attrib.pop('loadInfoIndex',None)

    # Cover selector authority.
    cc=root.find('./cover/coverConfigurations/coverConfiguration')
    if cc is None: raise RuntimeError('coverConfiguration missing')
    for old in list(cc):
        if old.tag=='cover': cc.remove(old)
    for i,stop in enumerate([0.0,0.2,0.4,0.6],start=1):
        attrs={'openAnimation':'loadingPipe','openAnimationStopTime':f'{stop:.3f}',
               'fillUnitIndices':str(i),'openOnBuy':'false','autoReactToTrigger':'false'}
        if i==4:
            attrs['closeAnimation']='loadingPipe'; attrs['closeAnimationStopTime']='1.000'
        ET.SubElement(cc,'cover',attrs)

    # Replace relevant loadingPipe parts but preserve donor sounds.
    anim=None
    for a in root.findall('./animations/animation'):
        if a.get('name')=='loadingPipe': anim=a; break
    if anim is None: raise RuntimeError('loadingPipe animation missing')
    sounds=[copy.deepcopy(c) for c in list(anim) if c.tag=='sound']
    for c in list(anim): anim.remove(c)

    parts=[]
    # Exact-root activation windows around selector stops.
    parts += [add_part(anim,'exactFillRootNodeTank1',0.20,0.40,startTrans=ACTIVE,endTrans=PARKED)]
    for tank,stop in [(2,2.0),(3,4.0),(4,6.0)]:
        parts.append(add_part(anim,f'exactFillRootNodeTank{tank}',stop-0.25,stop-0.10,startTrans=PARKED,endTrans=ACTIVE))
        parts.append(add_part(anim,f'exactFillRootNodeTank{tank}',stop+0.10,stop+0.25,startTrans=ACTIVE,endTrans=PARKED))

    # Explicit four-stop conveyor articulation. These are engineering keyframes, not a claim of runtime lock.
    states=[(0.0,TANK1_ANGLES),(2.0,TANK2_ANGLES),(4.0,TANK3_ANGLES),(6.0,TANK4_ANGLES),(10.0,TRANSPORT_ANGLES)]
    for idx in range(len(states)-1):
        t0,s0=states[idx]; t1,s1=states[idx+1]
        for j,node in enumerate(['overloadingArm01','overloadingArm02','overloadingArm03']):
            parts.append(add_part(anim,node,t0,t1,startRot=vecrot('y',s0[j]),endRot=vecrot('y',s1[j])))
        parts.append(add_part(anim,'overloadingArm04',t0,t1,startRot=vecrot('x',s0[3]),endRot=vecrot('x',s1[3])))

    # Preserve donor loading translation through Tank 4, then use donor-style stow translation.
    parts.append(add_part(anim,'overloadingArm04',0.0,6.0,startTrans='0 0.28 -0.074',endTrans='0 0.28 -0.074'))
    parts.append(add_part(anim,'overloadingArm04',6.0,9.6,startTrans='0 0.28 -0.074',endTrans='0 0.611 -0.005'))
    parts.append(add_part(anim,'overloadingArm04',9.6,10.0,startTrans='0 0.611 -0.005',endTrans='0 0.418 -0.045'))

    # Numeric flap authority: -100=open, 0=closed.
    parts += [
        add_part(anim,'tankFlapsFront',0.0,2.0,startRot='0 0 -100',endRot='0 0 -100'),
        add_part(anim,'tankFlapsFront',2.0,4.0,startRot='0 0 -100',endRot='0 0 0'),
        add_part(anim,'tankFlapsFront',4.0,10.0,startRot='0 0 0',endRot='0 0 0'),
        add_part(anim,'tankFlapsBack',0.0,2.0,startRot='0 0 0',endRot='0 0 0'),
        add_part(anim,'tankFlapsBack',2.0,4.0,startRot='0 0 0',endRot='0 0 -100'),
        add_part(anim,'tankFlapsBack',4.0,6.0,startRot='0 0 -100',endRot='0 0 -100'),
        add_part(anim,'tankFlapsBack',6.0,10.0,startRot='0 0 -100',endRot='0 0 0'),
    ]
    for p in parts: anim.append(p)
    for s in sounds: anim.append(s)

    # Replace old four load/unload mappings and add the new donor-safe mappings.
    mappings=root.find('./i3dMappings')
    if mappings is None: raise RuntimeError('i3dMappings missing')
    remove_ids={
        'unloadInfoSeeds','loadInfoSeeds','loadInfoFertilizer','unloadInfoFertilizer',
        'fillVolumeFlexTank4_UNUSED','fillVolumeTank4Flex',
        'loadInfoTank1','loadInfoTank2','loadInfoTank3','loadInfoTank4',
        'unloadInfoTank1','unloadInfoTank2','unloadInfoTank3','unloadInfoTank4',
    }
    for m in list(mappings):
        if m.tag=='i3dMapping' and m.get('id') in remove_ids:
            mappings.remove(m)
    for id_ in ['fillVolumeTank4Flex','loadInfoTank1','loadInfoTank2','loadInfoTank3','loadInfoTank4',
                'unloadInfoTank1','unloadInfoTank2','unloadInfoTank3','unloadInfoTank4']:
        ET.SubElement(mappings,'i3dMapping',{'id':id_,'node':mapping[id_]})

    return xml_bytes(root)

def patch_moddesc(data:bytes)->bytes:
    root=parse_xml(data)
    version=root.find('version')
    if version is not None: version.text='2.0.0.7'
    title=root.find('./title/en')
    if title is not None: title.text='Bourgault 3320-76 + 7950 Air Cart [4-Tank V7 Engineering]'
    desc=root.find('./description/en')
    if desc is not None:
        old=(desc.text or '').rstrip()
        desc.text=old+'\n\nV7 Engineering candidate:\n- Rebuilt four physical fill volumes including rear FLEX split.\n- Four load/unload positions front-to-rear.\n- Corrected front/rear lid authority.\n- Donor-validated distributed Tank 1 conveyor reach.\n- Realistic Seeder/custom-input compatibility bridge.\n'
    # Replace/insert project compatibility source registration.
    old_extra=root.find('extraSourceFiles')
    if old_extra is not None: root.remove(old_extra)
    extra=ET.Element('extraSourceFiles')
    ET.SubElement(extra,'sourceFile',{'filename':'scripts/FourTankCompat.lua'})
    children=list(root)
    store=root.find('storeItems')
    if store is not None:
        root.insert(children.index(store),extra)
    else:
        root.append(extra)
    return xml_bytes(root)

def sha256_file(path:str)->str:
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def default_lua_path()->str:
    repo_root=Path(__file__).resolve().parents[1]
    return str(repo_root/'scripts'/'compatibility'/'Bourgault7950FourTankCompat.lua')

def build(src:str,out:str,lua_path:str,allow_unknown_source:bool=False):
    source_sha=sha256_file(src)
    if source_sha != EXPECTED_SOURCE_SHA256 and not allow_unknown_source:
        raise RuntimeError(
            'Source archive SHA-256 does not match the verified V3 donor.\n'
            f'expected: {EXPECTED_SOURCE_SHA256}\n'
            f'found:    {source_sha}\n'
            'Refusing to apply geometry/path-specific V7 patch. '
            'Use --allow-unknown-source only for deliberate engineering comparison.'
        )
    if not os.path.isfile(lua_path):
        raise FileNotFoundError(f'compatibility Lua not found: {lua_path}')
    with open(lua_path,'rb') as f: lua=f.read()
    with zipfile.ZipFile(src,'r') as zin:
        i3d,mapping=patch_i3d(zin.read('i3d/Series_7950B.i3d'))
        vehicle=patch_vehicle(zin.read('xml/Series_7950B.xml'),mapping)
        moddesc=patch_moddesc(zin.read('modDesc.xml'))
        replacements={
            'i3d/Series_7950B.i3d':i3d,
            'xml/Series_7950B.xml':vehicle,
            'modDesc.xml':moddesc,
            'scripts/FourTankCompat.lua':lua,
        }
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as zout:
            seen=set()
            for info in zin.infolist():
                if info.filename=='scripts/FourTankCompat.lua': continue
                data=replacements.get(info.filename,zin.read(info.filename))
                zout.writestr(info,data)
                seen.add(info.filename)
            if 'scripts/FourTankCompat.lua' not in seen:
                # Use donor modDesc timestamp so the rebuilt archive is byte-reproducible
                # instead of embedding the wall-clock time of this build.
                moddesc_info=zin.getinfo('modDesc.xml')
                lua_info=zipfile.ZipInfo('scripts/FourTankCompat.lua', date_time=moddesc_info.date_time)
                lua_info.compress_type=zipfile.ZIP_DEFLATED
                lua_info.create_system=moddesc_info.create_system
                lua_info.external_attr=moddesc_info.external_attr
                zout.writestr(lua_info,lua)
    h=hashlib.sha256(open(out,'rb').read()).hexdigest()
    print(out)
    print('sha256',h)
    with zipfile.ZipFile(out) as z: print('entries',len(z.namelist()),'crc_bad',z.testzip())

def main():
    ap=argparse.ArgumentParser(
        description='Rebuild the Bourgault 7950B V7 engineering candidate from the verified V3 donor archive.'
    )
    ap.add_argument('source', help='verified Hispano V3 donor/candidate ZIP')
    ap.add_argument('output', nargs='?', default=DEFAULT_OUTPUT, help=f'output ZIP (default: {DEFAULT_OUTPUT})')
    ap.add_argument('--lua', default=None, help='V7 FourTankCompat.lua source; defaults to repository compatibility script')
    ap.add_argument(
        '--allow-unknown-source', action='store_true',
        help='bypass the exact donor SHA guard for deliberate engineering comparison only'
    )
    a=ap.parse_args()
    lua_path=a.lua or default_lua_path()
    build(a.source,a.output,lua_path,a.allow_unknown_source)
if __name__=='__main__': main()
