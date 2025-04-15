import pandas as pd
import matplotlib.pyplot as plt

from buglocator.evaluator import BugLocatorEvaluator
from bluir.evaluator import BluirEvaluator
from BRTracer.evaluator import BRTracerEvaluator
from VSM.evaluator import VSMEvaluator
from DreamLoc.evaluator import DreamLocEvaluator

projects = ["aspectj", "birt", "eclipse", "swt", "jdt", "tomcat"]
versions = ["baseline", "clean"]
techniques = ["VSM", "BugLocator", "BLUiR", "BRTracer", "DreamLoc"]
top_k = 1

def plot_graph(df, project, metric):
    plt.figure(figsize=(10, 6))
    colors = ['green' if diff > 0 else 'red' for diff in df["difference"]]
    plt.bar(df["Technique"], df["difference"], color=colors)
    plt.xlabel("Technique")
    plt.ylabel("Percentage change (%)")
    plt.title(f"Percentage Change (Cleaned vs Baseline) for {project}")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f"{project}_{metric}.png")

def do_for_accuracy():
    for project in projects:
        df = pd.DataFrame(columns=["technique", "baseline", "clean"])
        df["Technique"] = techniques
        for version in versions:
            values = []

            vsm = VSMEvaluator(
                f"/pub/ryasir/FL-VSM/results-{version}/{project}",
            )
            values.append(vsm.calculate_accuracy_at_k(top_k))

            buglocator = BugLocatorEvaluator(
                f"/pub/ryasir/FL-Buglocator/results-{version}/BugLocator_{project}",
                f"/pub/ryasir/FL-Buglocator/dataset/{project}-updated-data.xml"
            )
            values.append(buglocator.calculate_accuracy_at_k(top_k))

            bluir = BluirEvaluator(
                f"/pub/ryasir/FL-Bluir/results-{version}/BLUiR_{project}/recommended",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(bluir.calculate_accuracy_at_k(top_k))

            brtracer = BRTracerEvaluator(
                f"/pub/ryasir/FL-BRTracer/results-{version}/BRTracer_{project}",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(brtracer.calculate_accuracy_at_k(top_k))

            dreamloc = DreamLocEvaluator(
                f"/pub/ryasir/dream_loc/{project}_ranked_result_mapped.csv",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(dreamloc.calculate_accuracy_at_k(top_k))

            df[f"{version}"] = values

        df["difference"] =  (df["clean"] - df["baseline"]) / df["baseline"] * 100
        plot_graph(df, project, "accuracy")

def do_for_map():
    for project in projects:
        df = pd.DataFrame(columns=["technique", "baseline", "clean"])
        df["Technique"] = techniques
        for version in versions:
            values = []

            vsm = VSMEvaluator(
                f"/pub/ryasir/FL-VSM/results-{version}/{project}",
            )
            values.append(vsm.calculate_mean_average_precision_at_k(top_k))

            buglocator = BugLocatorEvaluator(
                f"/pub/ryasir/FL-Buglocator/results-{version}/BugLocator_{project}",
                f"/pub/ryasir/FL-Buglocator/dataset/{project}-updated-data.xml"
            )
            values.append(buglocator.calculate_mean_average_precision_at_k(top_k))

            bluir = BluirEvaluator(
                f"/pub/ryasir/FL-Bluir/results-{version}/BLUiR_{project}/recommended",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(bluir.calculate_mean_average_precision_at_k(top_k))

            brtracer = BRTracerEvaluator(
                f"/pub/ryasir/FL-BRTracer/results-{version}/BRTracer_{project}",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(brtracer.calculate_mean_average_precision_at_k(top_k))

            dreamloc = DreamLocEvaluator(
                f"/pub/ryasir/dream_loc/{project}_ranked_result_mapped.csv",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(dreamloc.calculate_mean_average_precision_at_k(top_k))

            df[f"{version}"] = values

        df["change"] =  (df["clean"] - df["baseline"]) / df["baseline"] * 100
        plot_graph(df, project, "map")

def do_for_mrr():
    for project in projects:
        df = pd.DataFrame(columns=["technique", "baseline", "clean"])
        df["Technique"] = techniques
        for version in versions:
            values = []

            vsm = VSMEvaluator(
                f"/pub/ryasir/FL-VSM/results-{version}/{project}",
            )
            values.append(vsm.calculate_mean_reciprocal_rank_at_k(top_k))

            buglocator = BugLocatorEvaluator(
                f"/pub/ryasir/FL-Buglocator/results-{version}/BugLocator_{project}",
                f"/pub/ryasir/FL-Buglocator/dataset/{project}-updated-data.xml"
            )
            values.append(buglocator.calculate_mean_reciprocal_rank_at_k(top_k))

            bluir = BluirEvaluator(
                f"/pub/ryasir/FL-Bluir/results-{version}/BLUiR_{project}/recommended",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(bluir.calculate_mean_reciprocal_rank_at_k(top_k))

            brtracer = BRTracerEvaluator(
                f"/pub/ryasir/FL-BRTracer/results-{version}/BRTracer_{project}",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(brtracer.calculate_mean_reciprocal_rank_at_k(top_k))

            dreamloc = DreamLocEvaluator(
                f"/pub/ryasir/dream_loc/{project}_ranked_result_mapped.csv",
                f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
            )
            values.append(dreamloc.calculate_mean_reciprocal_rank_at_k(top_k))

            df[f"{version}"] = values

        df["change"] =  (df["clean"] - df["baseline"]) / df["baseline"] * 100
        plot_graph(df, project, "mrr")

if __name__ == '__main__':
    do_for_accuracy()
    # do_for_map()
    # do_for_mrr()


