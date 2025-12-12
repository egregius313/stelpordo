using MediatR;
using Microsoft.AspNetCore.Mvc;
using StargateAPI.Business.Commands;
using StargateAPI.Business.Queries;
using System.Net;
using Microsoft.Data.Sqlite;
using System.Runtime.CompilerServices;

namespace StargateAPI.Controllers
{
   
    [ApiController]
    [Route("[controller]")]
    public class PersonController : ControllerBase
    {
        private readonly IMediator _mediator;
        public PersonController(IMediator mediator)
        {
            _mediator = mediator;
        }

        [HttpGet("")]
        public async Task<IActionResult> GetPeople()
        {
            try
            {
                var result = await _mediator.Send(new GetPeople()
                {

                });

                return this.GetResponse(result);
            }
            catch (Exception ex)
            {
                return this.GetResponse(new BaseResponse()
                {
                    Message = ex.Message,
                    Success = false,
                    ResponseCode = (int)HttpStatusCode.InternalServerError
                });
            }
        }

        [HttpGet("{name}")]
        public async Task<IActionResult> GetPersonByName(string name)
        {
            try
            {
                var result = await _mediator.Send(new GetPersonByName()
                {
                    Name = name
                });

                if (result.Person is null)
                {
                    return this.GetResponse(new BaseResponse()
                    {
                        Message = "No people found",
                        Success = false,
                        ResponseCode = (int)HttpStatusCode.NotFound
                    });
                }

                return this.GetResponse(result);
            }
            catch (Exception ex)
            {
                return this.GetResponse(new BaseResponse()
                {
                    Message = ex.Message,
                    Success = false,
                    ResponseCode = (int)HttpStatusCode.InternalServerError
                });
            }
        }

        [HttpPost("")]
        public async Task<IActionResult> CreatePerson([FromBody] string name)
        {
            try
            {
                var result = await _mediator.Send(new CreatePerson()
                {
                    Name = name
                });

                return this.GetResponse(result);
            }
            catch (Exception ex)
            {
                if (CausedByUniquenessConstraint(ex))
                {
                    return this.GetResponse(new BaseResponse()
                    {
                        Message = "Person with that name already exists",
                        Success = false,
                        ResponseCode = (int)HttpStatusCode.Conflict
                    });
                }

                return this.GetResponse(new BaseResponse()
                {
                    Message = ex.Message,
                    Success = false,
                    ResponseCode = (int)HttpStatusCode.InternalServerError
                });
            }
        }

        /// <summary>
        /// Checks if an exception was caused by a constraint violation in SQLite
        /// </summary>
        /// <param name="ex"></param>
        /// <returns></returns>
        private static bool CausedByUniquenessConstraint(Exception ex)
        {
            while (ex != null)
            {
                // Error code 19 is SQLITE_CONSTRAINT
                // https://www.sqlite.org/rescode.html#constraint
                // In this case, we assume that the constraint violation is due to uniqueness
                if (ex is SqliteException sqliteEx && sqliteEx.SqliteErrorCode == 19)
                {
                    return true;
                }
                ex = ex.InnerException;
            }
            return false;
        }
    }
}