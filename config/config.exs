use Mix.Config

config :phoenix, :json_library, Jason

config :bully,
  ecto_repos: [Bully.Repo]

import_config "#{Mix.env()}.exs"
