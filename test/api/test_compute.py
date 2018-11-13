from settings import environment, compute_arguments
from athera.api import compute

import unittest
import uuid
import time
from requests import codes


class ComputeTest(unittest.TestCase):

    # JOBS
    def test_get_jobs(self):
        """ Positive test """
        response = compute.get_jobs(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN
        )
        self.assertEqual(response.status_code, codes.ok)
        data = response.json()
        job_data = data['jobs']
        self.assertNotEqual(len(job_data), 0)
        first_job = job_data[0]
        self.assertNotEqual(len(first_job), 0)
        self.assertIn("id", first_job)
    
        # TODO check status filters

    def test_get_jobs_bad_group(self):
        """ Negative test - Confirm we handle bad group id """
        response = compute.get_jobs(
            environment.ATHERA_API_TEST_BASE_URL,
            "cheddar",
            environment.ATHERA_API_TEST_TOKEN
        )
        self.assertEqual(response.status_code, codes.internal_server_error)

    def test_get_jobs_wrong_group(self):
        """ Negative test - Confirm we cannot get jobs for a group we cannot access """
        response = compute.get_jobs(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_OTHER_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN
        )
        self.assertEqual(response.status_code, codes.forbidden)

    def test_get_job(self):
        """ Positive test """
        response = compute.get_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            environment.ATHERA_API_TEST_JOB_ID,
        )
        self.assertEqual(response.status_code, codes.ok)
        job_data = response.json()
        self.assertIn("id", job_data)
        self.assertEqual(environment.ATHERA_API_TEST_JOB_ID, job_data['id'])

    def test_get_job_wrong_job_id(self):
        """ Negative test - Confirm we cannot get a job which does not belong to us """
        response = compute.get_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            environment.ATHERA_API_TEST_OTHER_JOB_ID,
        )
        self.assertEqual(response.status_code, codes.not_found)

    def test_get_job_wrong_group_and_job_id(self):
        """ Negative test - Confirm we cannot get a job which does not belong to us via another group """
        response = compute.get_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_OTHER_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            environment.ATHERA_API_TEST_OTHER_JOB_ID,
        )
        self.assertEqual(response.status_code, codes.forbidden)

    def test_get_job_random_job_id(self):
        """ Negative test - Confirm we respond correctly to a non-existent job id """
        response = compute.get_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            str(uuid.uuid4())
        )
        self.assertEqual(response.status_code, codes.not_found)

    def test_get_job_bad_job_id(self):
        """ Negative test - Confirm we respond correctly to a broken id """
        response = compute.get_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            "stilton"
        )
        self.assertEqual(response.status_code, codes.bad_request)


    # PARTS
    def test_get_parts(self):
        """ Positive test """
        response = compute.get_parts(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            environment.ATHERA_API_TEST_JOB_ID,
        )
        self.assertEqual(response.status_code, codes.ok)
        data = response.json()
        part_data = data['parts'] 
        self.assertNotEqual(len(part_data), 0)
        first_part = part_data[0]
        self.assertNotEqual(len(first_part), 0)
        self.assertIn("id", first_part)

    def test_get_part(self):
        """ Positive test """
        response = compute.get_part(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            environment.ATHERA_API_TEST_JOB_ID,
            environment.ATHERA_API_TEST_PART_ID,
        )
        self.assertEqual(response.status_code, codes.ok)
        part_data = response.json()
        self.assertIn("id", part_data)
        self.assertEqual(environment.ATHERA_API_TEST_PART_ID, part_data['id'])

    def test_get_part_wrong_job_id(self):
        """ Negative test - Confirm we cannot get a part which does not belong to us """
        response = compute.get_part(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            environment.ATHERA_API_TEST_OTHER_JOB_ID,
            environment.ATHERA_API_TEST_OTHER_PART_ID,
        )
        self.assertEqual(response.status_code, codes.not_found)

    def test_get_part_wrong_group_and_job_id(self):
        """ Negative test - Confirm we cannot get a part which does not belong to us via its group """
        response = compute.get_part(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            environment.ATHERA_API_TEST_OTHER_JOB_ID,
            environment.ATHERA_API_TEST_OTHER_PART_ID,
        )
        self.assertEqual(response.status_code, codes.not_found)

    def test_get_part_random_id(self):
        """ Negative test - Confirm we respond correctly to a non-existent job id and part id """
        response = compute.get_part(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            str(uuid.uuid4()), 
            str(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, codes.not_found)


    # START JOB
    def test_start_job_and_get_part(self):
        """ Positive test - Nuke simply prints the help message and exits, ending the job (no need to stop) """
        payload = compute.make_job_request(
            environment.ATHERA_API_TEST_USER_ID, 
            environment.ATHERA_API_TEST_GROUP_ID, 
            environment.ATHERA_API_TEST_COMPUTE_APP_ID, 
            environment.ATHERA_API_TEST_COMPUTE_FILE_PATH, 
            "test_start_job_and_get_part_{}".format(hash(self)), 
            1, 2, 1, 
            environment.ATHERA_API_TEST_REGION, 
            compute_arguments,
        )
        response = compute.create_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            payload,
        )
        self.assertEqual(response.status_code, codes.ok)
        data = response.json()
        job_id = data['id']

        # Can take some time for the parts to be assigned
        timeout = 600
        interval = 10
        while timeout > 0:
            response = compute.get_parts(			
                environment.ATHERA_API_TEST_BASE_URL,
                environment.ATHERA_API_TEST_GROUP_ID,
                environment.ATHERA_API_TEST_TOKEN,
                environment.ATHERA_API_TEST_JOB_ID,
            )
            self.assertEqual(response.status_code, codes.ok)
            data = response.json()
            part_data = data['parts'] 
            print("{}s {}".format(timeout, len(part_data)))
            if len(part_data) > 0: 
                break
            timeout -= interval
            time.sleep(interval)
        self.assertGreater(timeout, 0)
            

    def test_start_job_incomplete_payload(self):
        """ Negative test - Send a incomplete payload """
        payload = compute.make_job_request("", "", "", "", "incomplete_payload", 0, 0, 0, "", ())
        response = compute.create_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            payload
        )
        self.assertEqual(response.status_code, codes.bad_request, "Create job with unexpected payload, unexpected status code {}".format(response.status_code))

    def test_start_job_bad_payload(self):
        """ Negative test - Send a junk payload """
        payload = {}
        response = compute.create_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            payload
        )
        self.assertEqual(response.status_code, codes.bad_request, "Create job with bad payload, unexpected status code {}".format(response.status_code))

    def test_start_job_wrong_group(self):
        """ Negative test - check we cannot launch a compute job in someone else's group """
        payload = compute.make_job_request(
            environment.ATHERA_API_TEST_OTHER_USER_ID, 
            environment.ATHERA_API_TEST_OTHER_GROUP_ID, 
            environment.ATHERA_API_TEST_COMPUTE_APP_ID, 
            environment.ATHERA_API_TEST_COMPUTE_FILE_PATH, 
            "test_start_job_wrong_group_{}".format(hash(self)), 
            1, 2, 1, 
            environment.ATHERA_API_TEST_REGION, 
            compute_arguments,
        )
        response = compute.create_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_OTHER_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            payload
        )
        self.assertEqual(response.status_code, codes.forbidden, "Create job unexpected status code {}".format(response.status_code))

    def test_start_and_stop_job(self):
        """ Positive test """
        payload = compute.make_job_request(
            environment.ATHERA_API_TEST_USER_ID, 
            environment.ATHERA_API_TEST_GROUP_ID, 
            environment.ATHERA_API_TEST_COMPUTE_APP_ID, 
            environment.ATHERA_API_TEST_COMPUTE_FILE_PATH, 
            "test_start_and_stop_job_{}".format(hash(self)), 
            1, 2, 1, 
            environment.ATHERA_API_TEST_REGION, 
            compute_arguments,
        )
        response = compute.create_job(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
            payload,
       )
        self.assertEqual(response.status_code, codes.ok, "Create job unexpected status code {}".format(response.status_code))
        job_data = response.json()
        job_id = job_data['id']


        # Wait until job status is ABORTED
        error_msg = self.wait_for_job_status(job_id, "CREATED")
        self.assertIsNone(error_msg, error_msg)
        
        # job_id = "d197b188-e57f-4a24-bd04-6bcfae5605b8"

        stop_job_attemps = 0
        while stop_job_attemps < 5:
            # Abort! Abort!
            response = compute.stop_job(
                environment.ATHERA_API_TEST_BASE_URL,
                environment.ATHERA_API_TEST_GROUP_ID,
                environment.ATHERA_API_TEST_TOKEN,
                job_id
            )
            print("Stop job attemp N.{}, status code={}".format(stop_job_attemps, response.status_code))
            if response.status_code == codes.ok:
                break
            stop_job_attemps += 1
            time.sleep(5)
        
        
        # Wait until job status is ABORTED
        error_msg = self.wait_for_job_status(job_id, "ABORTED")
        self.assertIsNone(error_msg, error_msg)

    def wait_for_job_status(self, job_id, desired_status):
        timeout = 100 # 1 minute
        job_status = ""
        wait_period = 10
        while timeout:
            response = compute.get_job(
                environment.ATHERA_API_TEST_BASE_URL,
                environment.ATHERA_API_TEST_GROUP_ID,
                environment.ATHERA_API_TEST_TOKEN,
                job_id,
            )
            self.assertEqual(response.status_code, codes.ok, "Get job unexpected status code {}".format(response.status_code))
            job_data = response.json()
            self.assertIn("id", job_data)
            self.assertEqual(job_id, job_data['id'])
            job_status = job_data['status'] 
            if job_status == desired_status:
                return None
            
            timeout -= wait_period
            time.sleep(wait_period)
        return "Waited {} seconds for jobs to reach status {}, but job has status {}".format(timeout, desired_status, job_status)