namespace StargateAPI.Business.Exceptions
{
    public class PersonDoesNotExistsExecption : Exception
    {
        public PersonDoesNotExistsExecption(string name) : base($"Person with name '{name}' does not exist.")
        {
        }

        public PersonDoesNotExistsExecption(string name, Exception innerException) : base($"Person with name '{name}' does not exist.", innerException)
        {
        }
    }
}