(defproject cloj "0.0.1"
  :description "Clojure workout"
  :license {:author "Dmitry Ponyatov"
            :email  "dponyatov@gmail.com"
            :year   2020}
  ;; :dev-dependencies [[lein-license "0.1.8"]]
  :url "https://www.youtube.com/watch?v=ciGyHkDuPAE"
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [org.clojure/java.jdbc "0.7.11"]
                 [org.xerial/sqlite-jdbc "3.34.0"]
                 [org.clojure/core.logic "1.0.0"]]
  ;; :main ^:skip-aot cloj.core
  ;; :target-path "target/%s"
  ;; :profiles {:uberjar {:aot :all}}
  :plugins [[org.clojars.benfb/lein-gorilla "0.6.0"]])
  