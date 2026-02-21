import os
import sys
# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.core.pipeline import Pipeline
from source.models.aircraft import AircraftConfiguration
from source.utils.logger import logger
import typer

app = typer.Typer()

@app.command()
def main(mode: str = typer.Option("default", help="Parser mode: default, vlm, ocr, extractor, hybrid")):
    # 1. Setup Test Data (Aircraft Fleet from Assessment)
    fleet = [
        AircraftConfiguration(model="MD-11", msn="48123"),
        AircraftConfiguration(model="DC-10-30F", msn="47890"),
        AircraftConfiguration(model="Boeing 737-800", msn="30123"),
        AircraftConfiguration(model="A320-214", msn="5234"),
        AircraftConfiguration(model="A320-232", msn="6789", modifications=["mod 24591 (production)"]),
        AircraftConfiguration(model="A320-214", msn="7456", modifications=["SB A320-57-1089 Rev 04"]), # Check logic for this
        AircraftConfiguration(model="A321-111", msn="8123"),
        AircraftConfiguration(model="A321-112", msn="364", modifications=["mod 24977 (production)"]),
        AircraftConfiguration(model="A319-100", msn="9234"),
        AircraftConfiguration(model="MD-10-10F", msn="46234"),
        # Verification examples
        AircraftConfiguration(model="MD-11F", msn="48400"),
        AircraftConfiguration(model="A320-214", msn="4500", modifications=["mod 24591 (production)"]),
        AircraftConfiguration(model="A320-214", msn="4500"), # Same MSN, different mods?
    ]

    # 2. Run Pipeline
    # Assuming PDFs are in 'data/raw'
    pipeline = Pipeline("data/raw")
    pipeline.ads_agent._mode(mode)
    results = pipeline.run(fleet)

    # 3. Print Results
    print("\n--- Evaluation Results ---")
    headers = ["Model", "MSN", "Mods"]
    ad_ids = list(results.keys())
    ad_ids.sort(reverse=True)
    headers.extend(ad_ids)
    
    # Simple table print
    header_str = f"{headers[0]:<15} | {headers[1]:<10} | {headers[2]:<25} | " + " | ".join(f"{hid:<25}" for hid in ad_ids)
    print(header_str)
    print("-" * len(header_str))

    for i, aircraft in enumerate(fleet):
        row = f"{aircraft.model:<15} | {aircraft.msn:<10} | {str(aircraft.modifications):<25} | "
        for ad_id in ad_ids:
            status = results[ad_id].get(i, "N/A")
            if status == "Affected":
                status_str = "✅ Affected"
            elif status == "Not Affected":
                status_str = "❌ Not affected"
            elif status == "Not Applicable":
                status_str = "❌ Not applicable"
            else:
                status_str = status
            row += f"{status_str:<18} | "
        print(row)

if __name__ == "__main__":
    app()
