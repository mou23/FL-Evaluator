import pandas as pd
import matplotlib.pyplot as plt

from buglocator.evaluator import BugLocatorEvaluator
from bluir.evaluator import BluirEvaluator
from BRTracer.evaluator import BRTracerEvaluator
from VSM.evaluator import VSMEvaluator
from DreamLoc.evaluator import DreamLocEvaluator

if __name__ == '__main__':
    projects = ["aspectj", "birt", "eclipse", "swt", "jdt", "tomcat"]
    versions = ["baseline", "clean"]
    techniques = ["VSM", "BugLocator", "BLUiR", "BRTracer", "DreamLoc"]
    top_k = 1

    for project in projects:
        df = pd.DataFrame(columns=["technique", "baseline", "clean"])
        df["Technique"] = techniques
        for version in versions:
            values = []

            vsm = VSMEvaluator(
                "/pub/ryasir/FL-VSM/results-{version}/BLUiR_{project}"
                "/pub/ryasir/FL-VSM/dataset/{project}-filtered.xml"
            )
            values.append(vsm.calculate_accuracy_at_k(top_k))

            buglocator = BugLocatorEvaluator(
                "/pub/ryasir/FL-Buglocator/results-{version}/Buglocator_{project}"
                "/pub/ryasir/FL-Buglocator/dataset/{project}-filtered.xml"
            )
            values.append(buglocator.calculate_accuracy_at_k(top_k))

            bluir = BluirEvaluator(
                "/pub/ryasir/FL-Bluir/results-{version}/BLUiR_{project}/recommended"
                "/pub/ryasir/FL-Bluir/dataset/{project}-filtered.xml"
            )
            values.append(bluir.calculate_accuracy_at_k(top_k))

            brtracer = BRTracerEvaluator(
                "/pub/ryasir/FL-BRTracer/results-{version}/BLUiR_aspectj/recommended"
                "/pub/ryasir/FL-BRTracer/dataset/{project}-filtered.xml"
            )
            values.append(brtracer.calculate_accuracy_at_k(top_k))

            dreamloc = DreamLocEvaluator(
                "/pub/ryasir/dream_loc/{project}_ranked_result_mapped.csv"
                "/pub/ryasir/FL-Bluir/dataset/{project}-filtered.xml"
            )
            values.append(dreamloc.calculate_accuracy_at_k(top_k))

            df[f"{version}"] = values

        df["difference"] = df["baseline"] - df["clean"]

        # Plot the difference values
        plt.figure(figsize=(10, 6))
        plt.bar(df["Technique"], df["difference"], color='skyblue')
        plt.xlabel("Technique")
        plt.ylabel("Difference (Baseline - Clean)")
        plt.title(f"Difference in Accuracy for Project: {project}")
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(f"{project}_difference_plot.png")

