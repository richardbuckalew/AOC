module day2


function get_input()
    open("day2.txt", "r") do io
        data = read(io, String)
        return data
    end
end

data = get_input()
lines = split(data, "\n")

A,R = let a = 0, r = 0
    for line in lines
        (length(line) == 0) && continue
        (L,W,H) = sort(parse.(Int, split(line, 'x')))
        a += 3*L*W + 2*W*H + 2*H*L
        r += 2L+2W+L*W*H
    end
    a,r
end
display((A, R))


end