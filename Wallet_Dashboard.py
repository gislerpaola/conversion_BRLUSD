import requests
import time
from web3 import Web3
from decimal import Decimal
from rich.console import Console
from rich.table import Table

# Constants
console = Console()
POLYGON_RPC_URL = "https://rpc.ankr.com/polygon"  # Or your preferred RPC URL
AAVE_PROTOCOL_DATA_PROVIDER_ADDRESS = "0xF71DBe0FAEF1473ffC607d4c555dfF0aEaDb878d"  # *** Double, triple CHECK this address! ***


def fetch_abi_from_polygonscan(contract_address):
    """Fetches the ABI from Polygonscan.
    Make sure to replace YOUR_POLYGONSCAN_API_KEY with a real API key
    """
    POLYGONSCAN_API_KEY = "DEAE3HA6TYV35YVRCGGTS6YPER544NNXZA"  # Insert your API Key

    url = f"https://api.polygonscan.com/api?module=contract&action=getabi&address={contract_address}&apikey={POLYGONSCAN_API_KEY}"
    try:
        # ADDED Wait time
        time.sleep(1)  # Wait for 1 second before making the request

        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data["status"] == "1":
            return data["result"]
        else:
            console.print(f"[bold red]Error fetching ABI: {data['message']}[/bold red]")
            return None
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Request error: {e}[/bold red]")
        return None


# List of Aave assets to track (MUST BE A-TOKEN ADDRESSES!)
AAVE_ASSET_ADDRESSES = [
    Web3.to_checksum_address("0x8E595469467662801F1943d5764A643f1e0da46a"),  # aMATIC (Verify this address!)
    Web3.to_checksum_address("0x3a58a54ff59d6314f726a83363c50d3b313ea54a"),  # aUSDC (Verify this address!)
    Web3.to_checksum_address("0x625E7708f293e5EA43646cC18D95F9D4536D805E"),  # aUSDT (Verify this address!)
    Web3.to_checksum_address("0xadc430fcbbcaaf869be395713ab2ca932180c23c")  # aWETH (Verify this address!)
]


def get_aave_data_provider(w3, abi):  # added ABI parameter
    return w3.eth.contract(
        address=w3.to_checksum_address(AAVE_PROTOCOL_DATA_PROVIDER_ADDRESS),
        abi=abi
    )


def fetch_aave_account_data(w3, wallet_address, asset_address, abi):
    if not Web3.is_address(wallet_address) or not Web3.is_address(asset_address):
        console.print(f"[bold red]Invalid wallet or asset address[/bold red]")
        return None

    data_provider = get_aave_data_provider(w3, abi)  # Correct ABI

    try:
        data = data_provider.functions.getUserReserveData(asset_address, wallet_address).call()

        if not isinstance(data, tuple):
            console.print(f"[bold red]Unexpected data type: {type(data)}. Expected a tuple.[/bold red]")
            return None

        return {
            "aTokenBalance": Decimal(data[0]) / Decimal(1e18),  # Adjust decimals based on the asset
            "stableDebt": Decimal(data[1]) / Decimal(1e18),
            "variableDebt": Decimal(data[2]) / Decimal(1e18),
            "isCollateral": data[8]
        }
    except Exception as e:
        console.print(
            f"[bold red]Error fetching Aave account data for {wallet_address} - {asset_address}: {e}[/bold red]")
        return None


# Function to display wallet data
def display_data(wallet_addresses, aave_protocol_data_provider_abi):
    w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))

    if not w3.is_connected():
        console.print("[bold red]Error: Could not connect to the Polygon blockchain.[/bold red]")
        return

    while True:
        console.clear()

        for wallet_address in wallet_addresses:
            try:
                wallet_address = Web3.to_checksum_address(wallet_address)
            except ValueError:
                console.print(f"[bold red]Invalid wallet address format: {wallet_address}[/bold red]")
                continue

            table = Table(title=f"Aave Balances for {wallet_address}")
            table.add_column("Asset", style="cyan")
            table.add_column("aToken Balance", style="yellow")
            table.add_column("Stable Debt", style="yellow")
            table.add_column("Variable Debt", style="yellow")
            table.add_column("Is Collateral", style="yellow")

            total_net_worth = Decimal(0)  # Initialize net worth
            for asset_address in AAVE_ASSET_ADDRESSES:
                try:
                    asset_address = Web3.to_checksum_address(asset_address)
                except ValueError:
                    console.print(f"[bold red]Invalid asset address format: {asset_address}[/bold red]")
                    continue

                aave_data = fetch_aave_account_data(w3, wallet_address, asset_address, aave_protocol_data_provider_abi)

                if aave_data:  # Check if data was fetched successfully
                    # In the real implementation, USD Conversion is important for calculating net worth.
                    net_worth = aave_data['aTokenBalance'] - aave_data['stableDebt'] - aave_data['variableDebt']
                    total_net_worth += net_worth

                    table.add_row(
                        asset_address,  # Display asset address (replace with asset symbol if available)
                        f"{aave_data['aTokenBalance']:.2f}",
                        f"{aave_data['stableDebt']:.2f}",
                        f"{aave_data['variableDebt']:.2f}",
                        str(aave_data['isCollateral'])
                    )

            table.add_row("Net Worth (no USD)", f"{total_net_worth:.2f}", style="bold green")
            console.print(table)

        time.sleep(60)  # Update every minute


if __name__ == "__main__":
    # Fetch the ABI from Polygonscan
    abi_json = fetch_abi_from_polygonscan(AAVE_PROTOCOL_DATA_PROVIDER_ADDRESS)
    if abi_json is None:
        console.print("[bold red]Failed to fetch ABI from Polygonscan. Exiting.[/bold red]")
        exit()

    wallets = input("Enter wallet addresses separated by commas: ").split(",")
    wallets = [wallet.strip() for wallet in wallets]
    display_data(wallets, abi_json)
