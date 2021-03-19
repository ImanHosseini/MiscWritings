open Format
open Core 
open Base
open Fn

(* Number of ways to distribute 'q' coins to 'n' person *)
let rec h (n,q) =
  match (n,q) with
  | (1,q) -> [[q]]
  | (n,q) -> List.concat (List.init (q+1) ~f:(fun r -> List.map ~f:(fun x -> List.append [r] x) (h (n-1, q-r))))
;;

(* Number of ways to distribute 'q' coins to 'n' person where each person gets less than 'l'*)
let rec hl (n,q,l) =
  match (n,q,l) with
  | (1,q,l) -> if q<l then [[q]] else []
  | (n,q,l) -> List.concat (List.init (min (q+1) l) ~f:(fun r -> List.map ~f:(fun x -> List.append [r] x) (hl (n-1, q-r, l))))
;;

(* Number of _acceptable_ distributions of 'c' person to 'p' coin types: the first person has more than any other person *)
let win (p,c) = 
  let l = (c + p - 1) / p in 
  let rng = List.range l (c+1) in
    List.fold_right ~f:(fun x acc -> acc @ (List.map ~f:(fun y -> x::y) (hl(p-1,c-x,x)))) ~init:([]) rng
;;

(* win(5,5);; *)