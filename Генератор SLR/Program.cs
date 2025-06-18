using SLRConverter;

class Program
{
    public static void Main(string[] args)
    {
        FileParser fileParser = new("input.txt", true);
        fileParser.ParseLinesToGrammarRules();
        fileParser.PrintGrammarRules();

        var table = SLRTableBuilder.Build(fileParser.GrammarRules);
        SLRTableCSVWriter.Write(table, "out.csv");

        TableSlider tableSlider = new();
        tableSlider.RunSlider(table);
        Console.WriteLine("Успех");

        return;
    }
}