import logging

from coreio.connect_spot import SpotConnection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

def main()->int:
    connection = SpotConnection()
    try:
        status = connection.verify_read_only_connection()
        print("Spot authentication test successful")
        print(f"Battery Count:{status['battery_count']}")
        print(f"Motor power state:{status['motor_power_state']}")
        return 0
    except Exception as error:
        logging.exception("Spot authentication test failed:%s", error)
        return 1
    finally:
        connection.shutdown()
    
if __name__=="__main__":
    raise SystemExit(main())