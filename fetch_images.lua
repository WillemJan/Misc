#!/usr/bin/env lua5.1

require "socket"

function recieve(connection)
    connection:settimeout(0)
    print(connection)
    local s, status, partial = connection:receive(2^20)
    if status == "timeout" then
        coroutine.yield(connection)
    end
    return s or partial, status
end

function download (host, url, path, basename, timestamp)
    local c = assert(socket.connect(host, 80))
    local count = 0
    c:send(string.format("GET http://%s/%s HTTP/1.0\r\n\r\n" , host, url))
    local out = assert(io.open(basename, "wba"))
    while true do
        local s, status, partial = recieve(c)
        count = count + #(s or partial)
        if status == "closed" then break end
        out:write(s or partial)
    end
    c:close()
    assert(out:close())
    local url = string.format("GET http://%s/%s HTTP/1.0\r\n\r\n" , host, url)
    print(url)
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

host = 'iot.fe2.nl'
path = '/tmp/'
timestamp = false


for i=0,4 do 
    url = string.format('/static/img/beach/beach%i.jpg', i)
    basename = string.format('beach%i.jpg', i)
    get(host, url, path, basename, timestamp)
end

dispatch()
