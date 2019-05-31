;; The background theory is linear integer arithmetic
(set-logic LIA)

;; Name and signature of the function to be synthesized
(synth-fun max2 ((z Int) (h Int)) Int

    ;; Define the grammar for allowed implementations of max2
    ((Start Int (z h 0 1
                 (+ Start Start)
                 (- Start Start)
                 (ite StartBool Start Start)))
    (StartBool Bool ((and StartBool StartBool)
                     (or StartBool StartBool)
                     (not StartBool)
                     (<= Start Start)
                     (= Start Start)
                     (>= Start Start))))
)

(declare-var x Int)
(declare-var y Int)

;; Define the semantic constraints on the function
(constraint (>= (max2 x y) x))
(constraint (>= (max2 x y) y))
(constraint (or (= x (max2 x y)) (= y (max2 x y))))

(check-synth)