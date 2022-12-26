module day4


using MD5

function get_input()
    open("input/day4.txt", "r") do io
        data = read(io, String)
        return data
    end
end

data = get_input()
lines = filter(x->length(x)>0, split(data, "\n"))

V = ['a','e','i','o','u']
bad = ["ab", "cd", "pq", "xy"]
function is_nice_old(s)
    (sum(count.(V, s))) < 3 && (return false)
    any(occursin.(bad, s)) && (return false)
    !any(diff(collect(s)) .== 0) && (return false)
    true
end

old_nice_count = sum(is_nice_old.(lines))


function repeating_pair(s)
    for i in 1:(length(s) - 1)
        (count(s[i:i+1], s) > 1) && (return true)
    end
    false
end

function sandwich(s)
    for i in 1:(length(s)-2)
        (s[i+2] == s[i]) && (return true)
    end
    false
end



is_nice(s) = (repeating_pair(s) && sandwich(s))

nice_count = sum(is_nice.(lines))

display(nice_count)




end