let n = int_of_string (input_line stdin) in
let a = int_of_string (input_line stdin) in

let mem = Hashtbl.create 1000 in
Hashtbl.add mem a true;
let mem_per_size = Hashtbl.create 1000 in
Hashtbl.add mem_per_size 1 a;

for size = 1 to 12 do
    for left_size = 1 to size-1 do
        let right_size = size - left_size in
        let left_function left = 
            let right_function right =
                for op = 0 to 3 do
                    let result = match op with
                        | 0 -> left + right
                        | 1 -> left - right
                        | 2 -> left * right
                        | _ -> if left mod right = 0 then left / right else 0
                    in
                    if result > 0 then (
                        if result == n then (
                            print_endline (string_of_int size);
                            exit 0;
                        );
                    
                        let found = Hashtbl.find_opt mem result in
                        if found = None then (
                            Hashtbl.add mem result true;
                            Hashtbl.add mem_per_size size result;
                        )
                    )
                done;
            in
            List.iter right_function (Hashtbl.find_all mem_per_size right_size);
        in
        List.iter left_function (Hashtbl.find_all mem_per_size left_size) ;
    done;
done;
