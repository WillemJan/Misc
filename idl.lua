#!/usr/bin/env lua5.1
require "socket"

function recieve(connection)
    connection:settimeout(0)
    local s, status, partial = connection:receive(2^20)
    if status == "timeout" then
        coroutine.yield(connection)
    end
    return s or partial, status
end

function download (host, url, path, basename, timestamp)
    local c = assert(socket.connect(host, 80))
    local count = 0
    basename = string.format("%s/%s.jpg", path, basename)
    local out = assert(io.open(basename, "wba"))

    local buffer = {}

    local go = false
    -- local test=  {}

    if timestamp == true then
        os.execute("mkdir -p " .. os.date("%d_%m_%Y"))
        local fname = string.format("%s/%s_%s.jpg", os.date("%d_%m_%Y"), os.date("%H:%M%S"), basename)
        out = assert(io.open(fname, "wba"))
    end

    local url = string.format("GET http://%s/%s HTTP/1.0\r\n\r\n" , host, url)
    c:send(url)
    while true do
        local s, status, partial = recieve(c)
        count = count + #(s or partial)
        if status == "closed" then break end
        -- test[#test + 1] = #(s or partial)
        -- print(string.find((s or partial), "Content-Type: image/jpeg"))
        if type(string.find((s or partial),'/jpeg'))  == "number" then
            go = true
        end
        if go == true then
            local buf = string.find((s or partial),'/jpeg')
            if type(string.find((s or partial),'/jpeg'))  == "number" then
                buf = lstring.find((s or partial),'/jpeg')
            end
            buffer[#buffer + 1] = (s or partial)
        end
    end
    c:close()
    out:write(table.concat(buffer))
    assert(out:close())
    
    -- for i, t in ipairs(test) do
    --     print(i, t)
    -- end
end

function get (host, url, path, basename, timestamp)
    local co = coroutine.create(
        function () download(host, url, path, basename, timestamp)
    end)
    table.insert(threads, co)
end

function dispatch ()
    local i = 1
    local connections = {}

    while true do
        if threads[i] == nil then
            if threads[1] == nul then break end
            i = 1
            connections = {}
        end
        local status, res = coroutine.resume(threads[i])
        if not res then
            table.remove(threads, i)
        else
            i = i + 1
            connections[#connections + 1] = res
            if #connections == #threads then
                socket.select(connections)
            end
        end
    end
end


threads = {}

host = 'www.scheveningenlive.nl'
path = './'
timestamp = false

images = {'cam_1.jpg', 'cam3.jpg', 'sport.jpg', 'cam2.jpg', 'pier.jpg'}

os.execute("rm -rf " .. os.date("%d_%m_%Y"))
os.execute("rm -rf *.jpg")

for i, image in ipairs(images) do 
    url = image
    basename = string.format('beach%i', i)
    get(host, url, path, basename, timestamp)
end

dispatch()
