module day1


function get_input()
    open("input/day1.txt", "r") do io
        data = read(io, String)
        return data
    end
end


data = get_input()

f = 0

for (i, c) in enumerate(data)
    global f
    f += Dict('(' => 1, ')' => -1)[c]
    if f < 0
        display(i)
        break
    end
end

display(f)



end