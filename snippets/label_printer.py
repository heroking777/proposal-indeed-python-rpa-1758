import pyautogui
import time

def automate_job_post_deletion():
    # Assuming the job posting is already open in a web browser
    # Wait for the page to load
    time.sleep(5)
    
    # Locate and click on the "削除" (Delete) button
    delete_button = pyautogui.locateOnScreen('delete_button.png')
    if delete_button:
        pyautogui.click(delete_button)
    else:
        print("Delete button not found")
        return
    
    # Wait for confirmation dialog to appear
    time.sleep(2)
    
    # Locate and click on the "OK" button in the confirmation dialog
    ok_button = pyautogui.locateOnScreen('ok_button.png')
    if ok_button:
        pyautogui.click(ok_button)
    else:
        print("OK button not found")
        return
    
    print("Job posting deleted successfully")

# Call the function to automate job post deletion
automate_job_post_deletion()
```

Note: This code uses the `pyautogui` library for screen automation. Ensure that you have the necessary images (`delete_button.png` and `ok_button.png`) in the same directory as your script or provide the correct path to these images. The script assumes that the job posting is already open in a web browser and that the "削除" (Delete) button and the "OK" button are visible on the screen. Adjustments may be needed based on the specific layout of the webpage.