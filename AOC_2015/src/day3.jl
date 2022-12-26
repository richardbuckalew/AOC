module day3


using MD5

function get_input()
    open("input/day3.txt", "r") do io
        data = read(io, String)
        return data
    end
end

# data = get_input()
# lines = split(data, "\n")
key = "ckczppom"


x = let i = 0
    while true
        s = key * string(i)
        h = bytes2hex(md5(s))
        ff = h[1:6]
        (ff=="000000") && break

        i += 1
        (i % 100000 == 0) && display(i)
    end
    i
end

display(x)



end