namespace StargateAPI.Business.Exceptions
{
    public class PersonAlreadyExistsExecption : Exception
    {
        public PersonAlreadyExistsExecption(string name) : base($"Person with name '{name}' already exists.")
        {
        }

        public PersonAlreadyExistsExecption(string name, Exception innerException) : base($"Person with name '{name}' already exists.", innerException)
        {
        }
    }
}