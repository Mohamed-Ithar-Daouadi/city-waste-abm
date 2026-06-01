from config import ALL_SCENARIOS
from model import CityWasteModel
from visualization import plot_results, print_summary_table


def run_scenario(config):
    print(f"\n Running: {config['name']} ({config['num_steps']} steps)...")
    model = CityWasteModel(config)

    for step in range(config["num_steps"]):
        model.step()
        if step % 50 == 0:
            print(f"     Step {step}/{config['num_steps']}")

    data = model.datacollector.get_model_vars_dataframe()
    print(f"Done: {config['name']}")
    return {"name": config["name"], "data": data}


if __name__ == "__main__":
    print("City Waste ABM Simulation\n")


    all_results = []
    for scenario in ALL_SCENARIOS:
        result = run_scenario(scenario)
        all_results.append(result)

    print_summary_table(all_results)
    plot_results(all_results)