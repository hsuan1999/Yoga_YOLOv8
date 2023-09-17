import math

class check_pose:
 
    @staticmethod
    def calculate_angle(landmark1, landmark2, landmark3):
        """
        Calculate the angle between three landmarks.

        Args:
            landmark1 (tuple): (x, y) coordinates of the first landmark.
            landmark2 (tuple): (x, y) coordinates of the second landmark (vertex).
            landmark3 (tuple): (x, y) coordinates of the third landmark.

        Returns:
            int: The angle in degrees.
        """
        # Calculate vectors between the landmarks
        vector1 = (landmark1[0] - landmark2[0], landmark1[1] - landmark2[1])
        vector2 = (landmark3[0] - landmark2[0], landmark3[1] - landmark2[1])

        # Calculate the dot product of the vectors
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        # Calculate the magnitudes of the vectors
        magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
        magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

        # Calculate the cosine of the angle using the dot product and magnitudes
        cosine_theta = dot_product / (magnitude1 * magnitude2)

        # Ensure that cosine_theta is within the valid range
        if -1 <= cosine_theta <= 1:
            # Calculate the angle in radians and convert to degrees
            angle_radians = math.acos(cosine_theta)
            angle_degrees = math.degrees(angle_radians)
        else:
            # Handle the case when cosine_theta is out of range
            angle_degrees = 0  # You can set a default value or handle it differently
        return int(angle_degrees)

    
    @staticmethod
    def check(pose_class, key_points):
            debug = True

            if isinstance(key_points,list) and len(key_points) == 34:

                # debug: print keypoint
                if debug:
                    for i in range(len(key_points)):
                        print(f'{i}: {key_points[i]}')
                # end

                nose = (key_points[0],key_points[1])
                left_eye = (key_points[2],key_points[3])
                right_eye = (key_points[4],key_points[5])
                left_ear = (key_points[6],key_points[7])
                right_ear    = (key_points[8],key_points[9])
                left_shoulder    = (key_points[10],key_points[11])  #5
                right_shoulder    = (key_points[12],key_points[13]) #6
                left_elbow    = (key_points[14],key_points[15])
                right_elbow    = (key_points[16],key_points[17])
                left_wrist    = (key_points[18],key_points[19])
                right_wrist    = (key_points[20],key_points[21])
                left_hip    = (key_points[22],key_points[23])   #11
                right_hip    = (key_points[24],key_points[25])  #12
                left_knee    = (key_points[26],key_points[27])
                right_knee    = (key_points[28],key_points[29])
                left_ankle    = (key_points[30],key_points[31])
                right_ankle    = (key_points[32],key_points[33])

                #身體中心線垂直偏移, (5,6)中點, (11,12)中點, (0,1)
                a = ((key_points[10]+key_points[12])/2, (key_points[11]+key_points[13])/2 )
                b = ((key_points[22]+key_points[24])/2, (key_points[23]+key_points[25])/2 )
                body_angle = check_pose.calculate_angle(a , b, (0,1)) 

                #髖部水平偏移: 
                hip_angle = check_pose.calculate_angle(left_hip , right_hip, (1,0))

                #左手肘: 5, 7 ,9
                left_elbow_angle = check_pose.calculate_angle(left_shoulder , left_elbow, left_wrist)

                #右手肘: 6, 8, 10
                right_elbow_angle = check_pose.calculate_angle(right_shoulder , right_elbow, right_wrist)

                #左膝: 11, 13, 15
                left_knee_angle = check_pose.calculate_angle(left_hip , left_knee, left_ankle)

                #右膝: 12, 14, 16
                right_knee_angle = check_pose.calculate_angle(right_hip , right_knee, right_ankle)


                match pose_class:
                    case 'ooo':
                        md = f'# {pose_class  }'
                                
                    case 'xxx':
                        md = f'# {pose_class  }'
                        
                    case _:
                        if pose_class == None:
                            md = '**未識別**<br><br>'
                        else:
                            md = f'**{pose_class}**<br><br>'
                        #    
                        md += f'身體中心線垂直偏移: {body_angle} 度<br>'
                        md += f'髖部水平偏移: {hip_angle} 度<br>'
                        md += f'左手肘: {left_elbow_angle} 度<br>'
                        md += f'右手肘: {right_elbow_angle} 度<br>'
                        md += f'左膝: {left_knee_angle} 度<br>'
                        md += f'右膝: {right_knee_angle} 度<br>'

            else:
                md = f'分類:{pose_class}<br>'
                md += 'keypoint error<br>' 
                md += '---'
                md += f'{key_points}<br>'                      

            if debug:
                print(md)

            return md
