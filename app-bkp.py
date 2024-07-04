from flask import Flask, render_template
from kubernetes import client, config

app = Flask(__name__)

# def load_config():
#     config.load_kube_config()
#     api_client = client.CoreV1Api()
#     return api_client
# current_config=load_config()
# print(current_config)
@app.route('/')
def index():
    try:
        # api_client = current_config 
        config.load_kube_config()
        api_client = client.CoreV1Api()
        # List all namespaces in the cluster
        namespaces = api_client.list_namespace()

        # Extract namespace names
        namespace_names = [ns.metadata.name for ns in namespaces.items]

        return render_template('ns.html', namespaces=namespace_names)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return f"Error: {error_message}", 500

@app.route('/<namespace_name>/deployments')
def deployments(namespace_name):
    try:
        config.load_kube_config()

        api_client = client.AppsV1Api()

        # List all deployments in the selected namespace
        deployments = api_client.list_namespaced_deployment(namespace_name)

       # print(deployments)
        # Extract image names from deployments
        deployment_images = []
        deployment_replicas = []
        deployment_names = []

        for deployment in deployments.items:
            deployment_names.append(deployment.metadata.name)
            deployment_replicas.append(deployment.spec.replicas)
            for container in deployment.spec.template.spec.containers:
                deployment_images.append(container.image)
        zipped_lists = zip(deployment_names, deployment_images, deployment_replicas)
        return render_template('deployment.html', deployments=zipped_lists, ns_name=namespace_name)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return f"Error: {error_message}", 500

# @app.route('/<deployment_name>/environment')
# def envs(deployment_name):


if __name__ == '__main__':
    app.run(debug=True)
