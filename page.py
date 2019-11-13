import cv2
import numpy as np
from sklearn.svm import SVC
import time

colors = {0: [255, 255, 255], 1: [200, 200, 200], 2: [154, 205, 50], 3: (0, 255, 255)}



class Page(object):
    size = 400


    def __init__(self, index, gaze, webcam, out):
        self.out = out
        self.page_index = index
        self.color_array = [0, 0, 0, 0, 1, 0]
        self.dominator_num = -1
        self.dominator_time = -1
        self.whe_initialized = 0
        self.gaze = gaze
        self.webcam = webcam
        if self.page_index == 0:
            self.page_transition = [1, 2, 3, 4, -3, 5, -1]
        elif self.page_index == 1 or self.page_index == 2 or self.page_index == 3 or self.page_index == 4:
            self.page_transition = [0, 0, 0, 0, -3, 0, 0]
        elif self.page_index == 5:
            self.page_transition = [6, 7, 8, 9, -3, 10, 0]
        else:  # 6, 7, 8, 9, 10
            self.page_transition = [0, 0, 0, 0, -3, 0, 5]

        self.add_key = []
        if self.page_index == 1:
            self.add_key = ["A", "C", "D", "E", "", "F"]
        elif self.page_index == 2:
            self.add_key = ["H", "I", "L", "M", "", "N"]
        elif self.page_index == 3:
            self.add_key = ["O", "R", "S", "T", "", "U"]
        elif self.page_index == 4:
            self.add_key = ["W", "Y", " ", "YES", "", "NO"]
        elif self.page_index == 6:
            self.add_key = ["B", "G", "J", "K", "", "P"]
        elif self.page_index == 7:
            self.add_key = ["Q", "V", "X", "Z", "", "0"]
        elif self.page_index == 8:
            self.add_key = ["1", "2", "3", "4", "", "5"]
        elif self.page_index == 9:
            self.add_key = ["6", "7", "8", "9", "", "I NEED HELP"]
        elif self.page_index == 10:
            self.add_key = ["I NEED FOOD", "I NEED WATER", "I WANT TO USE THE RESTROOM", "THANK YOU", "", "I LOVE YOU"]

        self.strings = []
        if self.page_index == 0:
            self.strings = \
                ["A C D\nE   F", "H I L\nM   N", "O R S\nT   U", "W Y Sp\nYes No", "", "Other\nNumbers \nShortcut"]
        elif self.page_index == 1 or self.page_index == 2 or self.page_index == 3 or self.page_index == 6 or \
                self.page_index == 7 or self.page_index == 8 or self.page_index == 9:
            self.strings = self.add_key
        elif self.page_index == 4:
            self.strings = ["W", "Y", "Sp", "YES", "", "NO"]
        elif self.page_index == 5:
            self.strings = \
                ["B G J\nK   P", "Q V X\nZ   0", "1 2 3\n4   5", "6 7 8\n9 HELP", "", "Shortcut"]
        elif self.page_index == 10:
            self.strings = \
                ["I NEED\nFOOD", "I NEED\nWATER", "I WANT TO\nUSE THE\nRESTROOM", "THANK\nYOU", "", "I LOVE\nYOU"]
        self.whe_break = False

    def run(self, str_display, out):
        self.out = out
        length_of_past = 30
        thresh_dominator_counts = 10
        thresh_of_center = 0.3
        threshold_of_dominator = 0.5

        stack_of_past = []
        state_count = np.zeros((7, 1))
        while True:
            next_index = self.page_index
            next_color = np.zeros((6, 1))

            _, frame = self.webcam.read()
            self.gaze.refresh(frame)
            frame = self.gaze.annotated_frame()

            if self.gaze.is_blinking:
                pass

            # 0, 1, 2, 3, 4, 5, 6 (eyes closed)
            current_look_at = int(self.gaze.current_gaze())

            if len(stack_of_past) < length_of_past:
                stack_of_past.append(current_look_at)
            else:
                temp = stack_of_past.pop(0)
                state_count[int(temp)] -= 1
                stack_of_past.append(current_look_at)
            state_count[current_look_at] += 1

            # check whether eyes closed is the dominator, no matter initialized or not
            print(np.max(state_count))
            print("whe_init", self.whe_initialized)

            print(state_count[4])
            if self.whe_initialized == 0:
                if state_count[4] >= length_of_past * thresh_of_center:
                    self.whe_initialized = 1

            if np.max(state_count) > length_of_past * threshold_of_dominator:
                this_dominator = np.where(state_count == np.max(state_count))[0]
                this_dominator = this_dominator[0]
                #print("#", str(this_dominator))
                #print("last", str(self.dominator_num))

                if this_dominator == 6: # eyes closed
                    if this_dominator == self.dominator_num:
                        self.dominator_time += 1
                    else:
                        self.dominator_time = 1
                        self.dominator_num = 6
                elif self.whe_initialized == 0:
                    if this_dominator == 4:
                        self.whe_initialized = 1
                        self.dominator_time = 0
                else:
                    if this_dominator == 4 or this_dominator == -1:
                        self.dominator_num = -1
                        self.dominator_time = 0
                    else:
                            #print("panduan:", str(this_dominator == self.dominator_num))
                        if this_dominator == self.dominator_num:

                            self.dominator_time = self.dominator_time + 1
                                #print("YESSS" + str(self.dominator_time))
                        else:
                                #print("AHHHHH")
                            self.dominator_num = this_dominator
                            self.dominator_time = 1
                    #print("time", str(self.dominator_time))

            if self.dominator_time > thresh_dominator_counts:
                next_index = self.page_transition[self.dominator_num]

            # string
            if next_index < 0:
                if len(str_display) > 0:
                    str_display = str_display[:-1]
            elif next_index == 0 and self.page_index is not 0 and self.dominator_num is not 6:
                str_display = str_display + self.add_key[self.dominator_num]

            # color array
            if self.whe_initialized == 0:
                if current_look_at == 4:
                    self.color_array = [0, 0, 0, 0, 3, 0]
                else:
                    self.color_array = [0, 0, 0, 0, 1, 0]
            else:
                self.color_array = [0, 0, 0, 0, 2, 0]
                if current_look_at is not 4 and current_look_at is not 6:
                    self.color_array[current_look_at] = 3
                if self.dominator_num is not -1 and self.dominator_num is not 6:
                    self.color_array[self.dominator_num] = 2

            if next_index != self.page_index:
                #print("Is this?")
                self.color_array = [0, 0, 0, 0, 1, 0]
                self.dominator_num = -1
                self.dominator_time = 0
                self.whe_initialized = 0
                break

            if next_index < 0:
                self.display(self.color_array, str_display, self.strings, frame)
            else:
                self.display(self.color_array, str_display, self.strings, frame)

            #cv2.putText(frame, str(current_look_at), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            #cv2.putText(frame, str(self.dominator_num), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            # cv2.waitKey(2)
            # cv2.imshow("demo", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.whe_break = True
                break

        if next_index < 0:
            return 0, str_display, self.whe_break
        else:
            return next_index, str_display, self.whe_break

    def initialization(self):
        list_name = ['up_left', 'up_center', 'up_right', 'left', 'center', 'right', ]
        iter_name = list_name.__iter__()
        name = iter_name.__next__()
        data_vertical = []
        data_horizontal = []
        dict_vertical = {}
        dict_horizontal = {}
        tot_L = 50 # 150
        std_horizontal = 0.3 # 0.07
        std_vertical = 0.6 # 0.2
        tempCounter = 0
        whe_sleep = 1

        while True:
            temp_color_arr = [0, 0, 0, 0, 0, 0]
            temp_color_arr[tempCounter] = 2
            temp_string_arr = ["", "", "", "", "", ""]
            temp_string_arr[tempCounter] = "Look\nHere"
            # self.display(temp_color_arr, "", temp_string_arr, frame)
            if whe_sleep == 1:
                time.sleep(2)
                whe_sleep = 0

            _, frame = self.webcam.read()

            # We send this frame to GazeTracking to analyze it
            self.gaze.refresh(frame)

            frame = self.gaze.annotated_frame()
            # cv2.imshow("initialization", frame)
            self.display(temp_color_arr, "", temp_string_arr, frame)


            if not (self.gaze.is_blinking is not None and self.gaze.is_blinking()) \
                    and self.gaze.horizontal_ratio is not None and \
                    self.gaze.blinking_ratio is not None:
                if len(data_horizontal) >= tot_L:
                    data_horizontal.pop(0)
                    data_vertical.pop(0)
                data_horizontal.append(self.gaze.horizontal_ratio)
                data_vertical.append(self.gaze.blinking_ratio)

            # start next name
            if len(data_vertical) >= tot_L and np.std(data_vertical) < std_vertical and len(
                    data_horizontal) >= tot_L and \
                    np.std(data_horizontal) < std_horizontal:
                dict_horizontal[name] = tuple(data_horizontal)
                dict_vertical[name] = tuple(data_vertical)
                # print(name, np.std(data_horizontal), np.std(data_vertical))
                data_horizontal = []
                data_vertical = []
                try:
                    name = iter_name.__next__()
                    tempCounter += 1
                    whe_sleep = 1
                except:
                    break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        x = []
        y = []
        tempI = 0
        for i in list_name:
            x = dict_horizontal[i]
            y = dict_vertical[i]
            xy = np.concatenate((np.array(x).reshape(tot_L, 1), np.array(y).reshape(tot_L, 1)), axis=1)
            if tempI == 0:
                data = xy
                tempI = 1
            else:
                data = np.concatenate((data, xy), axis=0)

        y = np.zeros((6 * tot_L, 1))
        for i in range(6):
            y[i * tot_L:(i + 1) * tot_L] = i
        y = np.ravel(y)
        clf = SVC(decision_function_shape='ovo')
        clf.fit(data, y)

        return clf

    def _create_new_image(self, color):
        im1 = np.ones((self.size, self.size, 3), np.uint8)
        return im1 * colors[color]

    def put_string(self, img, string):
        interval = 29
        iterr = iter(string)
        idx = 0
        tempory = ''
        dy = 50
        d = 0
        while(True):
            try:
                a = iterr.__next__()

                tempory = tempory + a
                idx += 1
                if len(tempory) % interval == 0 and idx != 0:
                    d += dy
                    cv2.putText(img, tempory, (0, d), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                        (147, 58, 31), 1)
                    tempory = ''
            except:
                d += dy
                cv2.putText(img, tempory,  (0, d), cv2.FONT_HERSHEY_DUPLEX, 1.2,
                            (147, 58, 31), thickness=4)
                break

        return img

    def display(self, color, string, text, frame):
        im = [0, 1, 2, 3, 4, 5]
        im[0] = self._create_new_image(color[0])
        im[1] = self._create_new_image(color[1])
        im[2] = self._create_new_image(color[2])
        im[3] = self._create_new_image(color[3])
        im[4] = self._create_new_image(color[4])
        im[5] = self._create_new_image(color[5])
        dy = 50
        for idx in range(6):
            if idx == 4:
                im[idx] = self.put_string(im[idx], string)
            else:
                for i, line in enumerate(text[idx].split('\n')):
                    # print(idx)
                    cv2.putText(im[idx], line, (int(self.size/3), int(self.size/3) + i * dy), cv2.FONT_HERSHEY_SIMPLEX, 1.2,  (147, 58, 31), thickness=4)

        partial1 = np.concatenate((im[0], im[3]))
        partial2 = np.concatenate((im[1], im[4]))
        partial3 = np.concatenate((im[2], im[5]))

        image = np.concatenate((partial1, partial2), axis=1)
        image = np.concatenate((image, partial3), axis=1)
        image = np.array(image, np.uint8)

        image = cv2.line(image, (self.size, 0), (self.size, self.size * 2), color=[0, 0, 0], thickness=3)
        image = cv2.line(image, (2 * self.size, 0), (2 * self.size, self.size * 2), color=[0, 0, 0], thickness=3)
        image = cv2.line(image, (0, self.size), (self.size * 3, self.size), color=[0, 0, 0], thickness=3)

        h, w, _ = frame.shape
        # print(frame.shape)
        image = cv2.resize(image, (w, h))
        frame = frame[:, ::-1, :]
        image = np.concatenate((image, frame), axis=1)
        # print(image.dtype)
        self.out.write(np.array(image))
        cv2.waitKey(2)
        cv2.imshow('test image', image)



# class Page:
#
#     def __init__(self, index, gaze, webcam, size=400):
#         self.page_index = index
#         self.dominator_num = -1
#         self.dominator_time = -1
#         self.whe_initialized = 0
#         self.gaze = gaze
#         self.webcam = webcam
#         self.size = size
#
#     def run(self):
#         pass
#
#     def _create_new_image(self, color):
#         im1 = np.ones((self.size, self.size, 3), np.uint8)
#         return im1 * colors[color]
#
#     def put_string(self, img, string):
#         interval = 29
#         iterr = iter(string)
#         idx = 0
#         tempory = ''
#         dy = 50
#         d = 0
#         while(True):
#             try:
#                 a = iterr.__next__()
#
#                 tempory = tempory + a
#                 idx += 1
#                 if len(tempory) % interval == 0 and idx != 0:
#                     d += dy
#                     cv2.putText(img, tempory, (0, d), cv2.FONT_HERSHEY_DUPLEX, 0.9,
#                         (147, 58, 31), 1)
#                     tempory = ''
#             except:
#                 d += dy
#                 cv2.putText(img, tempory,  (0, d), cv2.FONT_HERSHEY_DUPLEX, 0.9,
#                             (147, 58, 31), 1)
#                 break
#
#         return img
#
#     def display(self, color, text, string):
#         im = [0, 1, 2, 3, 4, 5]
#         im[0] = self._create_new_image(color[0])
#         im[1] = self._create_new_image(color[1])
#         im[2] = self._create_new_image(color[2])
#         im[3] = self._create_new_image(color[3])
#         im[4] = self._create_new_image(color[4])
#         im[5] = self._create_new_image(color[5])
#         dy = 50
#         for idx in range(6):
#             if idx == 4:
#                 im[idx] = self.put_string(im[idx], string)
#             else:
#                 for i, line in enumerate(text[idx].split('\n')):
#                     print(idx)
#                     cv2.putText(im[idx], line, (int(self.size/3), int(self.size/3) + i * dy), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
#
#         partial1 = np.concatenate((im[0], im[3]))
#         partial2 = np.concatenate((im[1], im[4]))
#         partial3 = np.concatenate((im[2], im[5]))
#
#         image = np.concatenate((partial1, partial2), axis=1)
#         image = np.concatenate((image, partial3), axis=1)
#         image = np.array(image, np.uint8)
#
#         image = cv2.line(image, (self.size, 0), (self.size, self.size * 2), color=[0, 0, 0])
#         image = cv2.line(image, (2 * self.size, 0), (2 * self.size, self.size * 2), color=[0, 0, 0])
#         image = cv2.line(image, (0, self.size), (self.size * 3, self.size), color=[0, 0, 0])
#
#         cv2.imshow('test image', image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#
#
#
# page = Page(1, 2, 3)
# text = ['asdf\nsdfas', 'asdfas', "asdfas\nsd\nasdf", "asdf", "asd\nk", "asdf\n"]
# color = ["yellow", "green", "gray", "white", "yellow", "yellow"]
# Page.display(page, color, text, 'stringstringstringstringstringstringstring')
