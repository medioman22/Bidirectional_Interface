using UnityEngine;

public class DroneCamera : MonoBehaviour
{
    // Camera will follow target with following speed (dep. smoothing factor), keeping the initial offset 
    public Transform Target;
    public Transform camTransform;
    private Vector3 Offset;
    public float SmoothTime = 0.3f;
    private Vector3 velocity = Vector3.zero;

    // For camera rotation
    private float cameraViewRotation = 0.0f;
    private float oldCameraViewRotation = 0.0f;
    private float fixedYaw = 1.0f;
    private float r = 1.0f;

    public float observationInputRotation = 0.0f;
    public float controllerRotationSpeed = 0.5f;

    private PositionControl dronePositionControl;
    private VelocityControl droneVelocityControl;

    private void Start()
    {
        // Keeping the same offset
        Offset = camTransform.position - Target.position;

        // For camera rotation
        dronePositionControl = GetComponent<PositionControl>();
        droneVelocityControl = GetComponent<VelocityControl>();

        if (dronePositionControl.controlYaw)
        {
            cameraViewRotation = camTransform.eulerAngles.y;
            oldCameraViewRotation = cameraViewRotation;

            fixedYaw = transform.eulerAngles.y;
            dronePositionControl.targetYaw = fixedYaw;
        }
    }

    private void LateUpdate()
    {
        // update position
        Vector3 targetPosition = Target.position + Offset;
        
        camTransform.position = Vector3.Lerp(camTransform.position, targetPosition, SmoothTime);

        // update rotation
        if (dronePositionControl.controlYaw)
        {
            observationInputRotation = transform.eulerAngles.y;
            droneVelocityControl.desiredYawRate = r * controllerRotationSpeed;
            dronePositionControl.targetYaw = r * fixedYaw;
        }
    }
}