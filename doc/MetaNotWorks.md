# Metaprogramming not works

My idea with metaprogramming via source code generation tends not works due to
the unpredicted complexity rise while I'm trying to reimplement the `metaL`
system itself via circular description.

* If you use dumb code strings, you found yourself in double code coping, which
  is more problematic than classical copy & paste programming.
* In contrast, if you try to use complex code abstractions such as class models,
  the complexity is rising faster than you produce generated code.
