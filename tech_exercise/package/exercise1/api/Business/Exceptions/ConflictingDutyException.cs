namespace StargateAPI.Business.Exceptions
{
    public class ConflictingDutyException : Exception
    {
        public ConflictingDutyException(string name) : base($"Person '{name}' already has a duty assigned.")
        {
        }

        public ConflictingDutyException(string name, Exception innerException) : base($"Person with name '{name}' already has a duty assigned.", innerException)
        {
        }
    }
}