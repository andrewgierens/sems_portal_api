# SEMS Portal

## Description
SEMS Portal is a simple wrapper designed to interact with various APIs exposed by a specific website. It simplifies the process of sending requests and handling responses, making it easier for developers to integrate and work with the available services.

## Getting Started

### Prerequisites
Before you begin, ensure you have met the following requirements:
- Python version >=3.5

### Installation
To install SEMS Portal API, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/andrewgierens/sems_portal_api.git
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
To use SEMS Portal, you need to have Python and `aiohttp` installed. Here’s a quick example to get you started:

```python
import aiohttp
import asyncio
from sems_portal_api import login_to_sems, set_region

async def main():
    set_region('eu')
    async with aiohttp.ClientSession() as session:
        account = "your_account"
        password = "your_password"
        
        data = await login_to_sems(session, account, password)
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
```

In this example, we import the required modules and define an `async` main function. Inside this function, we create an `aiohttp.ClientSession`, which is used to send an HTTP request to the SEMS portal for logging in. Replace `"your_account"` and `"your_password"` with your actual login credentials.

The `login_to_sems` function takes three parameters: the session, account, and password, and it returns the data received from the SEMS portal. The returned data is then printed to the console.


For testing the demo account credentials may be used:
```python
account = "demo@goodwe.com"
password = "GoodweSems123!@#"
```

## Contributing
Contributions to SEMS Portal are welcome and appreciated. If you have any suggestions or bug reports, please open an issue in the repository.
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License
This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact
If you have any questions or want to reach out, you can contact me at apgierens@gmail.com
