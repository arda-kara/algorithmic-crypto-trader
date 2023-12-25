---

# Cryptocurrency Trading Bot for Binance

## Overview
This script is an automated trading bot designed for the Binance cryptocurrency exchange. It uses the Binance API to conduct trades based on the Relative Strength Index (RSI) strategy, targeting the BTCUSDT trading pair by default. The bot is equipped with features for RSI calculation, automated trade execution, and logging of trading activities.

## Features
- **Binance API Integration**: Interacts with Binance for trading operations.
- **RSI-Based Trading Strategy**: Utilizes the Relative Strength Index (RSI) for making trading decisions.
- **Automated Trading**: Continuously monitors market conditions and executes trades.
- **Account and Log Management**: Manages a virtual trading account and logs activities.

## Prerequisites
Before running this script, ensure you have the following installed:
- Python 3.x (preferably 3.8, 3.9, or 3.10)
- `pandas` and `pandas_ta` for data manipulation and technical analysis
- Binance API Python client (`binance.client`)

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Install Dependencies:**
   ```bash
   pip install pandas pandas_ta python-binance python-decouple
   ```

3. **API Configuration:**
   - Obtain your Binance API Key and Secret Key.
   - Store them securely using the `decouple` library.

## Configuration
- Set the trading pair, log paths, and RSI thresholds in the script.
- The bot operates in test mode by default. Change to live mode cautiously.

## Usage
Run the script with:
```bash
python trading_bot.py
```
Monitor the log files for trading activities and errors.

## Disclaimer
- This bot is for educational purposes only. Do not use it for live trading without thorough testing.
- Cryptocurrency trading involves significant risk. We are not responsible for any financial losses.

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/arda-kara/algorithmic-crypto-trader/issues) if you want to contribute.

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Arda Kara – ardakara1881@hotmail.com

Project Link: [https://github.com/arda-kara/algorithmic-crypto-trader](https://github.com/arda-kara/algorithmic-crypto-trader)

---
