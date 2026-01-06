import os
import json
import argparse
from dataclasses import dataclass, field


@dataclass
class ClassifiedObs:
    """
    Observations according to their classification results.
    """

    tp_obs: list = field(default_factory=list)
    fp_obs: list = field(default_factory=list)
    fn_obs: list = field(default_factory=list)
    sub_obs: list = field(default_factory=list)

    def __add__(self, other):
        return ClassifiedObs(
            tp_obs=self.tp_obs + other.tp_obs,
            fp_obs=self.fp_obs + other.fp_obs,
            fn_obs=self.fn_obs + other.fn_obs,
            sub_obs=self.sub_obs + other.sub_obs,
        )


@dataclass
class ClassificationStats:
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    ref_obs: int = 0
    hyp_obs: int = 0

    def set_empty_expected_and_observed(self):
        self.f1 = 1.0
        self.recall = 1.0
        self.precision = 1.0

    def set_empty_expected(self):
        self.f1 = 0.0
        self.recall = 1.0
        self.precision = 0.0

    def set_empty_observed(self):
        self.f1 = 0.0
        self.recall = 0.0
        self.precision = 1.0

    def calc(self, classified_obs: "ClassifiedObs"):
        tp = len(classified_obs.tp_obs)
        fp = len(classified_obs.fp_obs)
        fn = len(classified_obs.fn_obs)
        self.ref_obs = tp + fn
        self.hyp_obs = tp + fp
        self.recall = 0.0 if tp == 0.0 else tp / (tp + fn)
        self.precision = 0.0 if tp == 0.0 else tp / (tp + fp)
        try:
            self.f1 = 2 * (self.precision * self.recall) / (self.precision + self.recall)
        except ZeroDivisionError:
            self.f1 = 0.0


def json_values_equal(observed, expected):
    # If types mismatch, we can stop right away, unless we're dealing
    # with numerics, which we can coerce for scoring purposes
    observed_is_numeric = isinstance(observed, int) or isinstance(observed, float)
    expected_is_numeric = isinstance(expected, int) or isinstance(expected, float)
    if (
        not isinstance(observed, type(expected))
        and not (observed_is_numeric and expected_is_numeric)
    ):
        return False
    # Check types
    if isinstance(expected, str):
        # There might be some string comparison rabbit hole here vs C# - check

        # If the observed is a single list of 1 string, convert to string
        if isinstance(observed, list) and len(observed) == 1 and isinstance(observed[0], str):
            observed = observed[0]

        # If expected is spelled-out 'Fahrenheit' or 'Celsius', convert to 'F' or 'C'
        if expected.lower() == 'fahrenheit':
            expected = 'F'
        elif expected.lower() == 'celsius':
            expected = 'C'

        return observed == expected
    elif isinstance(expected, int) or isinstance(expected, float):
        return float(observed) == float(expected)
    elif isinstance(expected, bool):
        return bool(observed) == bool(expected)
    elif expected is None or not expected:
        return True
    elif isinstance(expected, dict):
        # Check keys
        observed_keys = list(observed.keys())
        expected_keys = list(expected.keys())
        if len(observed_keys) != len(expected_keys):
            return False
        if set(observed_keys) != set(expected_keys):
            return False
        observed_keys.sort()
        expected_keys.sort()
        for key in observed_keys:
            if not json_values_equal(observed[key], expected[key]):
                return False
        return True
    elif isinstance(expected, list):
        if len(observed) != len(expected):
            return False
        observed.sort()
        expected.sort()
        for i in range(len(observed)):
            if not json_values_equal(observed[i], expected[i]):
                return False
        return True
    else:
        raise ValueError(f'Something went wrong in json_values_equal: {observed}, {expected}')


def unroll_observations(obs_list):
    obs_dict = {}
    for obs in obs_list:
        if obs['id'] not in obs_dict:
            obs_dict[obs['id']] = []
        if obs["value_type"] != "MULTI_SELECT":
            obs_dict[obs['id']].append(obs)
        else:
            if isinstance(obs["value"], list):
                value_temp = obs["value"].copy()
                for value in value_temp:
                    obs_temp = obs.copy()
                    obs_temp["value"] =  value
                    obs_dict[obs['id']].append(obs_temp)
            else:
                obs_dict[obs['id']].append(obs)
    return obs_dict


def classify_observations(classified_obs, predicted_by_ids, expected_by_ids):
    predicted_by_ids_dict = unroll_observations(predicted_by_ids['observations'])
    expected_by_ids_dict = unroll_observations(expected_by_ids['observations'])
    for ids, predicted_observations_for_id in predicted_by_ids_dict.items():
        for i, predicted_observation in enumerate(predicted_observations_for_id):
            predicted_matched_expected = False

            for expected_observation in expected_by_ids_dict.get(ids, []):

                if predicted_observation["id"] == expected_observation["id"] and json_values_equal(predicted_observation['value'], expected_observation['value']):
                    predicted_matched_expected = True

                if predicted_matched_expected:
                    classified_obs.tp_obs.append(predicted_observation)
                    matching_exp = expected_observation
                    break

            if not predicted_matched_expected:
                classified_obs.fp_obs.append(predicted_observation)
            else:
                expected_by_ids_dict[ids].remove(matching_exp)

    for obs_id, expected_obs in expected_by_ids_dict.items():
        for ob in expected_obs:
            classified_obs.fn_obs.append(ob)

    return classified_obs


__doc__ = """
script to calculate scores for MEDIQA-SYNUR challenge
"""
def main():

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-r", "--reference", help="input .json of reference observations", required=True)
    parser.add_argument("-p", "--predicted", help="input .json of predicted observations", required=True)
    parser.add_argument("-o", "--output", help="output metrics file", default=None)
    args = parser.parse_args()
    reference = {}
    with open(args.reference, 'r') as handle:
        for line in handle:
            file_id = json.loads(line)
            reference[file_id["id"]] = file_id

    candidates = {}
    with open(args.predicted, 'r') as handle:
        for line in handle:
            file_id = json.loads(line)
            candidates[file_id["id"]] = file_id
    classified_obs = ClassifiedObs()
    for id in reference:
        if id in candidates:
            classified_obs = classify_observations(classified_obs, candidates[id], reference[id])
    final_results = ClassificationStats()
    final_results.calc(classified_obs)

    print("Final Results:")
    print(final_results.precision)
    print(final_results.recall)
    print(final_results.f1)

    if args.output is not None:
        outfile = os.path.join(args.output, "scores.json")
        print("Writing results to ", outfile)

        out_dict = {k: v for k, v in final_results.__dict__.items() if not k.startswith('_')}
        with open(outfile, 'w') as out_handle:
            json.dump(out_dict, out_handle)

if __name__ == "__main__":
    main()
