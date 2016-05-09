defmodule MessageBusSpec do
  use ESpec
  example_group do
    context "It should instantiate a list of channels" do
      it do: expect :list |> to(be_array)
    end
  end
end
