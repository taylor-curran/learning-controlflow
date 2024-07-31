from snowflake_blocks import SnowflakeConnection

# Create an instance with necessary configurations
snowflake_conn = SnowflakeConnection()

# Save the instance with a specific name
snowflake_conn.save(name="my-snowflake-conn", overwrite=True)

print("Snowflake Connection block saved successfully!")
