local zlib = require("zlib")

local FN = assert(arg[1])
local OUT = arg[2] or "."

local r
local uint32 = function() return string.unpack("I", r:read(4)) end
local uint16 = function() return string.unpack("H", r:read(2)) end
local uint8  = function() return string.unpack("B", r:read(1)) end

r = assert(io.open(FN, "rb"))

assert("RP6L" == r:read(4))

print("header", r:seek())
local header = {
    version = uint32(),
    c1 = uint8(),
    c2 = uint8(),
    c3 = uint8(),
    c4 = uint8(),
    parts = uint32(),
    sections = uint32(),
    files = uint32(),
    fnames_sz = uint32(),
    fnames = uint32(),
    unk = uint32(), -- ???
}

print("section", r:seek())
local section = {}
for i = 1, header.sections do
    local s = {}
    s.filetype = uint8()
    s.type2 = uint8()
    s.type3 = uint8()
    s.type4 = uint8()
    s.offset = uint32()
    s.unpackedSize = uint32()
    s.packedSize = uint32()
    s.unk1 = uint32()
    table.insert(section, s)
end

print("parts", r:seek())
local filepart = {}
for i = 1, header.parts do
    local p = {}
    p.sectionIndex = uint8() +1
    p.unk1 = uint8()
    p.fileIndex = uint16() +1
    p.offset = uint32()
    p.size = uint32()
    p.unk2 = uint32()
    table.insert(filepart, p)
end

print("filemap", r:seek())
local filemap = {}
for i = 1, header.fnames do
    local m = {}
    m.partsCount = uint8()
    m.unk1 = uint8()
    m.filetype = uint8()
    m.unk2 = uint8()
    m.fileIndex = uint32() +1
    m.firstPart = uint32() +1
    table.insert(filemap, m)
end

print("fidx", r:seek())
local fname_idx = {}
for i = 1, header.fnames do
    fname_idx[i] = uint32()
end

local fname_off = r:seek()
print("fnames", fname_off)
local filename = {}
for i = 1, #fname_idx do
    r:seek("set", fname_off + fname_idx[i])
    local chars = {}
    while true do
        local char = r:read(1)
        if char == "\x00" then break end
        table.insert(chars, char)
    end
    local name = table.concat(chars)
    filename[i] = name
end

print("data", r:seek())


local strfmt = [[
ver: %d, compress: %02d-%02d-%02d-%02d
parts: %d, sections: %d, files: %d, fnames: %d/%d, block: %d
]]
print(strfmt:format(
        header.version, header.c1, header.c2, header.c3, header.c4,
        header.parts, header.sections, header.files,
        header.fnames_sz, header.fnames, header.unk))

--[[
print("#      ft1 ft2 ft3 ft4     offset   unpacked     packed unknown")
for i = 1, #section do
    local s = section[i]
    print(("s%05d %3d %3d %3d %3d %10d %10d %10d %d"):format(
            i, s.filetype, s.type2, s.type3, s.type4,
            s.offset, s.unpackedSize, s.packedSize, s.unk1))
end
print()

print("#     sidx unk  fidx        off        unp unk2")
for i = 1, #filepart do
    local p = filepart[i]
    print(("p%05d %3d %3d %5d %10d %10d %d"):format(
            i, p.sectionIndex, p.unk1, p.fileIndex, p.offset, p.size, p.unk2))
end
print()

print("#     prts unk ftp unk    fileidx      first")
for i = 1, #filemap do
    local m = filemap[i]
    print(("m%05d %3d %3d %3d %3d %10d %10d"):format(
            i, m.partsCount, m.unk1, m.filetype, m.unk2, m.fileIndex, m.firstPart))
end
print()
]]

for i = 1, #section do
    local s = section[i]
    local pack = s.packedSize
    local unpk = s.unpackedSize
    r:seek("set", s.offset)
    print("s"..i, pack, unpk, pack > 0 and "packed" or "not packed")
    local data = r:read(unpk)
    if pack > 0 then
        s.data = zlib.inflate()(data)
    else
        s.data = data
    end
end

r:close()


require("mod_dds_header")
local dds = DDSHeader

local fmt = {
    [2] = Format_RGBA, --bpp 32
    [3] = Format_RGBA, --bpp 32
    [14] = Format_DXT3,
    [17] = Format_DXT1,
    [18] = Format_DXT3,
    [19] = Format_DXT5,
    [33] = Format_DXT5,
}

local function process_texture(data)
    local width = string.unpack("H", data:sub(1, 2))
    local height = string.unpack("H", data:sub(3, 4))
    local mips = string.unpack("H", data:sub(9, 12))
    local dxt = string.unpack("I", data:sub(13, 16))
    --print("\n"..width, height, mips, dxt)
    
    local dxtfmt = fmt[dxt]
    assert(dxtfmt, dxt)
    local bpp = (2 == dxt or 3 == dxt) and 32 or 16
    
    dds:new()
    local t = {}
    t[1] = dds:generate(width, height, mips, dxtfmt, bpp)
    t[2] = data:sub(152, -1)
    return table.concat(t)
end


local data
for i = 1, header.fnames do
    local ext
    local e = filemap[i].filetype
    if     16 == e then ext = "msh"
    elseif 32 == e then ext = "dds" --"tex"
    elseif 48 == e then ext = "shd"
    elseif 64 == e then ext = "anm"
    elseif 80 == e then ext = "fx"
    else                ext = tostring(e)
    end

    local fn = filename[i] ..".".. ext
    local m = filemap[i]
    local ptr = m.firstPart --+1
    
    io.write(i, "\\", header.fnames, "\t", fn, ": ")
    local w = assert(io.open(OUT .."/".. fn, "w+b"))

    local count = m.partsCount
    local out = {}
    while count > 0 do
        local p = filepart[ptr]
        local sidx = p.sectionIndex --+1
        local size = p.size
        local s = section[sidx]
        local sect = s.filetype
        local offs = p.offset

        io.write("+", sect)
        table.insert(out, s.data:sub(offs+1, offs+size))

        ptr = ptr + 1
        count = count - 1
    end
    print()
    
    out = table.concat(out)
    if 32 == e then
        out = process_texture(out)
    end
    w:write(out)
    w:close()
end
