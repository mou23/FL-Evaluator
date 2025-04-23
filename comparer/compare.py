import sys
import pandas as pd

from buglocator.evaluator import BugLocatorEvaluator
from bluir.evaluator import BluirEvaluator
from BRTracer.evaluator import BRTracerEvaluator
from VSM.evaluator import VSMEvaluator
from DreamLoc.evaluator import DreamLocEvaluator

dreamloc_mp = {
    "aspectj": ("AspectJ.xml", 220),
    "birt": ("Birt.xml", 1879),
    "eclipse": ("Eclipse_Platform_UI.xml", 2116),
    "jdt": ("JDT.xml", 2110),
    "swt": ("SWT.xml", 1971),
    "tomcat": ("Tomcat.xml", 405)
}

def create_evaluators(project, version):
    evaluators = [
        VSMEvaluator(
            f"/pub/ryasir/FL-VSM/results-{version}/{project}",
        ),
        BugLocatorEvaluator(
            f"/pub/ryasir/FL-Buglocator/results-{version}/BugLocator_{project}",
            f"/pub/ryasir/FL-Buglocator/dataset/{project}-updated-data.xml"
        ),
        BluirEvaluator(
            f"/pub/ryasir/FL-Bluir/results-{version}/BLUiR_{project}/recommended",
            f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
        ),
        BRTracerEvaluator(
            f"/pub/ryasir/FL-BRTracer/results-{version}/BRTracer_{project}",
            f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
        ),
    ]
    if version == "baseline":
        evaluators.append(DreamLocEvaluator(
            f"/pub/ryasir/original_results_dreamloc/{project}_ranked_result_mapped.csv",
            f"/pub/ryasir/FL-Bluir/dataset/{project}-updated-data.xml"
        ))
    else:
        evaluators.append(DreamLocEvaluator(
            f"/pub/ryasir/dream_loc/{project}_ranked_result_mapped.csv",
            f"/pub/ryasir/dream_loc/data/reports/{dreamloc_mp[project]}",
            dreamloc_mp[project][1]
        ))

    return evaluators

def compute_metric(metric_name, evaluator, top_k):
    method_map = {
        "accuracy": evaluator.calculate_accuracy_at_k,
        "map": evaluator.calculate_mean_average_precision_at_k,
        "mrr": evaluator.calculate_mean_reciprocal_rank_at_k
    }
    return method_map[metric_name](top_k)

if __name__ == '__main__':
    projects = ["aspectj", "birt", "eclipse", "swt", "jdt", "tomcat"]
    versions = ["baseline", "clean"]
    techniques = ["VSM", "BugLocator", "BLUiR", "BRTracer", "DreamLoc"]

    usage = "Usage: python compare.py <metric>(accuracy, map, mrr) <top_k> (1, 5, 10)"
    if len(sys.argv) != 2:
        print(usage)
        sys.exit(1)

    if sys.argv[1] not in [1, 5, 10] \
        or sys.argv[2] not in ["accuracy", "map", "mrr"]:
        print(usage)
        sys.exit(1)

    metric = sys.argv[1]  # accuracy, map, mrr
    top_k = int(sys.argv[2])

    for project in projects:
        df = pd.DataFrame(columns=["Technique"] + versions)
        df["Technique"] = techniques

        for version in versions:
            evaluators = create_evaluators(project, version)
            df[version] = [compute_metric(metric, ev, top_k) for ev in evaluators]

        df["change"] = (df["clean"] - df["baseline"]) / df["baseline"] * 100
        df.to_csv(f"{project}_{metric}_k@{top_k}.csv", index=False)
