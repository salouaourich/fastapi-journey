# DECISIONS

## Field Types

I used integer for id because each patient must have a unique identifier.

The name field uses string with min_length to ensure the name is not empty.

Age is constrained with gt and lt to prevent unrealistic ages.

Appointments is a list because one patient can have multiple appointments.

## Validation Rules

min_length ensures names are not too short.

Age validation prevents negative ages or unrealistic values.

Enum ensures appointment type can only be specific values.

## Async Endpoint

The GET /patients/ endpoint uses asyncio.sleep(1) to simulate a real database request delay.