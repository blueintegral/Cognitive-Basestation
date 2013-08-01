;;; Module that just re-exports the level_swig module

(define-module (gnuradio level)
  #:use-module (gnuradio export-safely)
  #:use-module (gnuradio level_swig)
  #:duplicates (merge-generics replace check))

(re-export-all '(gnuradio level_swig))