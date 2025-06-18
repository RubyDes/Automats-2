using LLConverter_1;

class Program
{
    public static void Main(string[] args)
    {
        FileParser fileParser = new("input.txt", false);
        fileParser.ParseLinesToGrammarRules();
        fileParser.PrintGrammarRules();

        LLTableBuilder builder = new();
        Table table = builder.Build(fileParser.GrammarRules);

        LLTableCSVWriter.Write(table, "output.csv");

        try
        {
            TableSlider slider = new("rules.txt");
            slider.RunSlider(table);

            Console.WriteLine("Успешно");
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.ToString());
        }
    }
}