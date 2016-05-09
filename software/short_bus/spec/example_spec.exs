defmodule ExampleSpec do
  use ESpec

  before do
    answer = Enum.reduce((1..9), &(&2 + &1)) - 3
    {:shared, answer: answer} #saves {:key, :value} to `shared`
  end

  example "test" do
    expect shared.answer |> to(eq 42)
  end

  context "Defines context" do
    subject(shared.answer)

    it do: is_expected.to be_between(41, 43)

    describe "is an alias for context" do
      before do
        value = shared.answer * 2
        {:shared, new_answer: value}
      end

      let :val, do: shared.new_answer

      it "checks val" do
        expect val |> to(eq 84)
      end
    end
  end

  xcontext "xcontext skips examples." do
    xit "And xit also skips" do
      "skipped"
    end
  end

  pending "There are so many features to test!"
end
