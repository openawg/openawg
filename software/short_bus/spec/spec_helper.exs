ESpec.configure fn(config) ->
  config.before fn ->
    {:shared, hello: :world}
  end

  config.finally fn(_shared) ->
    :ok
  end
end
