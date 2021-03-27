# Clojure {#clj}

* generative metaprogramming
    * host language: Clojure
    * multiple target languages:
        * Python | Django
        * Erlang/Elixir | Phoenix
        * Rust
        * embedded C/C++
* deployment platforms:
    * VPS / generic Linux
    * embedded Linux (Buildroot)
    * Cortex-M embedded devices (STM32)
* final programming model:
    * bootstrap via system self-application
    * distributed object runtime for Web and IoT applications
    * language model mixes elements of Smalltalk, Python, Elixir, and Clojure
* interactive programming
    * http://gorilla-repl.org/

## generic code templating and inheritance

an open set of hypotheses

* most projects share a lot of code
    * code can be inherited between projects as constant or parametric code
      snippets
* coding patterns and algorithms stays more or less the same between multiple
  programming languages
    * code generation can be used for transforming algorithm defined in a
      generic form, into multiple target languages
    * code patterns can be distilled from some concrete code into a generic form
      and shared and reused between many projects
* some languages lacks of code checking facilities
    * generic code analyzer can improve code quality, and increase the
      programmer productivity via minimizing debug efforts
* every programming language stack has its own pros and cons
    * these features can be migrated to any required language
        * by reimplementing them and adding as automated boilerplate code, and/or
        * via using of emulating virtual machine (interpreter)
* such alike *generic code manipulation system* can be usable in a real contract work
    * without implementing anything from the above
    * it works even at the level of string interpolation/concatenation and
      writing of plain text files
    * it can be used only in the mode of grossmeister's *secret weapon* because
      the volume of knowledge and understanding which you must transfer to your
      colleagues makes it impossible to share
        * rich and deep documenting definitely does not help due to the increase
          of complexity introduced by this documenting
        * never ever speak about you use such a system with anybody, especially
          with your colleagues or employer because it scares them


### terms

* **code distilling**
    - reimplementing some feature again and again in the trying to found the
      most stable code form
* **host language**
    - the programming language in which code transformations are written
        * it must be flexible and dynamic as much as possible
        * it does not matter how it is memory effective, or fast
        * the best variant for the host language is the Lisp dialect even with
          its alien's syntax
            * I myself fought a lot with recommendations of Lisp for this task,
              but practice shows it's the truth -- while you are trying to use
              any other human-friendly host language like Python, finally you
              are finding yourself in implementing your own Lisp on objects 8)
            * The program self-application and self-modification is the
              must-have property, including first-class macroses, and language
              orientation especially on the AST-like data structure
              transformations.
            * Clojure is good here because it has multiple parens types, it is
              more or less known and mature language closer to the mainstream,
              and it internally works over objects & JVM stack.
            * JVM integration lets you use any mature tools from the Java world,
              targets on compiler design or code analysis, such as ANTLR, Graal,
              Java-based IDE integration, GUI/visualization, etc. Also, you can
              directly generate bytecode and run it on JVM as the off-the-shelf
              runtime.
* **target language**
    any language in which you generates the code, and next runs the
* **backend-compiler** (or interpreter)
    - mainstream language compiler which builds distribution binary or script
      package


## Clojure

* https://www.youtube.com/watch?v=ciGyHkDuPAE
* [Введение в Clojure](http://alexott.net/ru/clojure/clojure-intro/)

### miniKanren

* http://minikanren.org
* https://www.codewars.com/kata/5a0e6c62ba2a143015000001
  * https://github.com/swannodette/logic-tutorial
  * https://github.com/clojure/core.logic/wiki/A-Core.logic-Primer

##  Python

### Django

##  Erlang/Elixir

* Саша Юрич [Elixir в действии](https://www.ozon.ru/context/detail/id/164833016/)

### Phoenix

## Rust

* [The Rust Programming Language](https://doc.rust-lang.org/book/)
  * [Язык программирования Rust](https://doc.rust-lang.ru/book/)
* https://github.com/chimez/clojure-rust

## embedded C/C++

### Cortex-M (STM32)

#### STM32F030F4P6 blue pill /Cortex-M0/

#### STM32F103C8T6 blue pill /Cortex-M3/

### embedded Linux

#### Buildroot


## Clojure как noSQL in-memory СУБД

* https://news.ycombinator.com/item?id=19727843

```
Dmitry Ponyatov, [18.12.20 22:40]

а видел кто-нибудь статьи, рассматривающие кложу или лисп не как язык программирования, а с точки зрения "это такая хитрая in-memory no-SQL СУБД на (само)вычисляемых данных" ?

чтобы ломать у питонистов/жавистов блокировку на принятиё ее как средства разработки

предлагаешь такой использовать, они начинают вопить "что это за инопланетная херня?!"

а ты в ответ: ну вот смотри, ты же не пытаешься на SQL сайты писать, и применять свои ООПшные привычки?

теперь берём noSQL, там тоже нет такого, чтобы из классов мухоморы строить, это тоже такая специфичная среда вещь в себе, возможностей побольше чем в табличных БД, и язык свой специфический

ну вот, и на Лисп/Кложу — тоже смотри как на некий движок БД, только он умеет данные не просто хранить, и делать по ним поиск, но и вычислять новые по старым

ну а чтобы вычислять, нужен какой-то способ определить способ этого вычисления — для этого как раз функции и есть

только это не те функции как в питоне — любая функция это такой же блок данных, только движок БД умеет этот блок выполнять внутри себя, подавать на вход исходные данные, и полученные новые данные хранить

и система заточена на работу с контейнерами данных, как в обычных языках программирования — списки, массивы, скаларяные значения типа числел и строк, и всякие развесистые стуктуры, которые из этого всего можно налепить

ну и определение функции — тоже в этот набор входит, в виде вложенного списка, только движок БД её может выполнять (через интерпретацию)

а поскольку всё это поверх JVM крутится, можно налепить интерфейсы с чем-угодно, не используя больше никакой внешний язык программирования типа Python/Django которые обычно используются для построения интерфейса между СУБД, пользователем, и внешними сервисами

Clojure это своего рода движок БД, причём настолько мощный и расширяемый, что позволяет прямо на нём строить программные системы

ну например, те же MySQL/Postgres имеют средства подключения к другим СУБД в виде external table — и тут также можно делать, только из JVM доступны все её низкоуровневые фичи вплоть до сокетов + можно прицеплять любые Java-библиотеки, вообще любые

мне просто кажется, что если с такой точки зрения рассматривать — у обычного императивного пхпшника не будет срабатывать "ой вай еще один язык учить, да ещё такой шизнутый"

они уже привыкли, что когда начинаешь работать с какой-нибудь странной штукой типа Mongo или GraphQL, приходится её собственный язык осваивать, и это в общем и не сложно — ну да, еще один специфический синтаксис, приходится что-то почитать, может даже в чужом коде покопаться

но при этом не срабатывает рефлекс попыток натягивания совы на Pythonские привычки, и воплей "да тут классов вообще нет! как этим пользоваться вообще можно?"

а с другой стороны — нет соблазна делать на этом вообще всё, как бы у каждого типа СУБДшки есть своя какая-то ниша приложений: кто-то под реляционку и табличныые данные десятилетиями затачивалось, кто-то с деревьями удобно шуршит, в кого-то можно логи терабайтами совать и оно там чего-то себе может посчитать по ним

ну вот у Clojure тоже своя ниша — ворочать сложные многосвязные структуры данных, не слишком большого объема (чтобы в ОЗУ умещались), и одновременно можно на этом изобразить сервер приложений, и запхать туда на Java что угодно если уже готовых встроенных средств не хватило
```

### Telegram posts

https://t.me/LanguageDev/21258

`Ilmir:`

Разумеется, я не могу говорить за всех - у нас для этого есть @relizarov (но он,
похоже, ливнул из чата). Моё мнение - в будущем, непонятно, насколько скором,
такие вещи будут доступны любому. К сожалению, один язык может покрыть
потребности всех пользователей только если он расширяем. Уже есть подобное в
других языках в виде макросов и компиляторных плагинов. Единственное отличие
Котлина в таком случае - это малокровная поддержка в ИДЕ. Когда я писал свой
компиляторный плагин, после его написания поддержка в ИДЕ, гредле и мавене
свелось к примерно 10-20 строк на каждый из плагинов. Разумеется, в случае
фейсбучного плагина поддержка в ИДЕ потребовала немного больше усилий.

`Dmitry:`

Расширяемый язык и IDE?.. Косясь на clojure... не, ну наф наф! Повторить подвиг,
и вырастить ещё одного еМакса Франкенштейновича -- это надо хорошо упороться.
Хороша кложка к обеду, но не до такой же степени :)

`Vladimir Kazanov:`

Ну вроде Емакс жил, живет и здравствует; да и clojure тоже. Опять же, visual
studio code, который как бы емакс-на-js, тоже в полном порядке.

Чем вас расширяемые редакторы и языки не устраивают?

`Dmitry:`

Наоборот, только на них и можно толком работать, не вырывая волосы.
Но их достоинство одновременно является и недостатком — чуть шаг влево вправо от
компьюнити, и всё (библиотеки, расширения) нужно писать самому. По крайней мере,
это возможно т.к. система открытая.

Проблема: требуется определённый уровень от программиста, я вот только-только до
Лиспа созрел, и то только потому что 
* (а) самое главное: придумал как встроить любой странный язык в рабочий
    процесс, но не тащить его в прод (достаточно только ядра языка без либ и
    фреймворков)
* (б) сам подолбался со своим языком пока не понял что я похоже всё время
    пытаюсь переизобрести что-то, но мешает синтаксис и хочется что-то
    лиспоподобное с прямой работой с АСТ
* (в) обошёл ментальный блок, рассматривая Лисп не как язык, а как такой особый
    вид нереляционной СУБД для структур данных — с этой т.з. не хочется
    натягивать привычную сову на новый синтаксис и семантику, имея бэкграунд что
    каждая СУБД имеет свою узкую область использования, и свой уникальный
    языковой интерфейс

ЗЫ: прикольная очепятка, не буду исправлять

`Dmitry:`

(а) **компиляторы стремятся строить бимодульно из бэкенда и фронтенда, с языками можно сделать то же самое**

* **фронт-язык** — пишете на чём хотите, 
  - любые извращения Lisp/Clojure, Haskell, Smalltalk,... 
  - чем динамичнее тем лучше, причём удобнее без типов, 
  - в идеале с REPL, 
  - производительность и потребляемые ресурсы практически не важны
* **бэк-компилятор/интерпретатор**
  - то что вам диктует рынок/работодатель/заказчик/легаси, 
  - наоборот чем больше проверки кода тем лучше (навороченные типы, линтеры,
    стат.анализаторы)
