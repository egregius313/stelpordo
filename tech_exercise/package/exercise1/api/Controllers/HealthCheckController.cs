using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace StargateAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class HealthCheckController : ControllerBase
    {
        private readonly IMediator _mediator;
        public HealthCheckController(IMediator mediator)
        {
            _mediator = mediator;
        }

        [HttpGet("")]
        public IActionResult HealthCheck()
        {
            return this.GetResponse(new BaseResponse()
            {
                Message = "API is running",
                Success = true,
                ResponseCode = 200
            });
        }
    }
}