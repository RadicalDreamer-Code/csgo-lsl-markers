# csgo-lsl-markers

Send event-timestamps/markers to your lsl stream from the CS:GO game state integration

## Simple usage
Copy the **gamestate_integration_GSI.cfg** file to *C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\csgo\cfg*

Create a **.env** file inside the project root folder and add following data:

```py
key=S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9
```
The key needs to be the same inside the .cfg file in order for the authentication to work.

Use the *subscribe*-decorator from EventFlags() to pass the event values to a function that gets triggered if any event change happen.

```py
event_flags = EventFlags()

@event_flags.subscribe
def write_to_csv(event: Event):
    csv_writer.write_to_csv(event)
```