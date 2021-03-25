defmodule Metal do
  use Application
  # @impl true
  def start(_type, _args) do
    children = []
    opts = [strategy: :one_for_one, name: Metal.Supervisor]
    Supervisor.start_link(children, opts)
  end

  def hello do
    :world
  end

  IO.puts "Hello"

  list = [1, 2, 3, 4]
  list |> List.delete_at(-1)
  list ++ [1]
end
