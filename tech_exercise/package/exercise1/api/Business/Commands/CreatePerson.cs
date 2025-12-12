using MediatR;
using MediatR.Pipeline;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using StargateAPI.Business.Data;
using StargateAPI.Business.Exceptions;
using StargateAPI.Controllers;

namespace StargateAPI.Business.Commands
{
    public class CreatePerson : IRequest<CreatePersonResult>
    {
        public required string Name { get; set; } = string.Empty;
    }

    public class CreatePersonPreProcessor : IRequestPreProcessor<CreatePerson>
    {
        private readonly StargateContext _context;
        public CreatePersonPreProcessor(StargateContext context)
        {
            _context = context;
        }
        public Task Process(CreatePerson request, CancellationToken cancellationToken)
        {
            var person = _context.People.AsNoTracking().FirstOrDefault(z => z.Name == request.Name);

            if (person is not null) throw new BadHttpRequestException("Bad Request");

            return Task.CompletedTask;
        }
    }

    public class CreatePersonHandler : IRequestHandler<CreatePerson, CreatePersonResult>
    {
        private readonly StargateContext _context;

        public CreatePersonHandler(StargateContext context)
        {
            _context = context;
        }
        public async Task<CreatePersonResult> Handle(CreatePerson request, CancellationToken cancellationToken)
        {

                var newPerson = new Person()
                {
                   Name = request.Name
                };

                try
                {
                    await _context.People.AddAsync(newPerson);

                    await _context.SaveChangesAsync();                
                } catch (Exception ex)
                {
                    if (CausedByUniquenessConstraint(ex))
                    {
                        throw new PersonAlreadyExistsExecption(request.Name, ex);
                    }
                    throw;
                }

                return new CreatePersonResult()
                {
                    Id = newPerson.Id
                };
          
        }

        /// <summary>
        /// Checks if an exception was caused by a constraint violation in SQLite
        /// </summary>
        /// <param name="ex"></param>
        /// <returns></returns>
        private static bool CausedByUniquenessConstraint(Exception ex)
        {
            // https://www.sqlite.org/rescode.html#constraint
            const int SQLITE_CONSTRAINT = 19;
            const int SQLITE_CONSTRAINT_UNIQUE = 2067;

            while (ex != null)
            {
                if (ex is SqliteException sqliteEx && sqliteEx.SqliteErrorCode == SQLITE_CONSTRAINT && sqliteEx.SqliteExtendedErrorCode == SQLITE_CONSTRAINT_UNIQUE)
                {
                    return true;
                }
                ex = ex.InnerException;
            }
            return false;
        }
    }

    public class CreatePersonResult : BaseResponse
    {
        public int Id { get; set; }
    }
}
