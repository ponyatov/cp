use Mix.Config

config :bully, Bully.Repo,
  username: "bully",
  password: "bully",
  database: "bully_phx",
  hostname: "localhost",
  show_sensitive_data_on_connection_error: true,
  pool_size: 10
