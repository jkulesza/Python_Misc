import matplotlib as mpl

def def_parula():

    parula = [
    (53, 42, 134, 255),
    (53, 43, 137, 255),
    (53, 45, 141, 255),
    (53, 46, 144, 255),
    (53, 48, 147, 255),
    (54, 49, 150, 255),
    (54, 51, 153, 255),
    (54, 52, 156, 255),
    (54, 54, 159, 255),
    (54, 55, 162, 255),
    (53, 57, 165, 255),
    (53, 59, 169, 255),
    (53, 60, 172, 255),
    (52, 62, 175, 255),
    (51, 63, 178, 255),
    (51, 65, 181, 255),
    (50, 67, 185, 255),
    (48, 68, 188, 255),
    (47, 70, 191, 255),
    (45, 72, 194, 255),
    (44, 74, 197, 255),
    (41, 75, 201, 255),
    (39, 77, 204, 255),
    (36, 79, 207, 255),
    (33, 82, 210, 255),
    (29, 84, 213, 255),
    (25, 86, 216, 255),
    (20, 88, 218, 255),
    (16, 91, 220, 255),
    (12, 93, 222, 255),
    (8, 94, 223, 255),
    (5, 96, 224, 255),
    (3, 98, 224, 255),
    (2, 99, 225, 255),
    (1, 101, 225, 255),
    (1, 102, 225, 255),
    (1, 103, 225, 255),
    (1, 104, 225, 255),
    (2, 106, 224, 255),
    (2, 107, 224, 255),
    (3, 108, 224, 255),
    (4, 109, 223, 255),
    (5, 110, 223, 255),
    (6, 111, 223, 255),
    (7, 112, 222, 255),
    (8, 113, 222, 255),
    (10, 114, 221, 255),
    (11, 115, 221, 255),
    (12, 116, 220, 255),
    (13, 117, 220, 255),
    (13, 118, 219, 255),
    (14, 119, 219, 255),
    (15, 120, 218, 255),
    (16, 121, 217, 255),
    (16, 122, 217, 255),
    (17, 123, 216, 255),
    (18, 123, 216, 255),
    (18, 124, 215, 255),
    (19, 125, 215, 255),
    (19, 126, 214, 255),
    (19, 127, 214, 255),
    (19, 128, 213, 255),
    (20, 129, 213, 255),
    (20, 130, 212, 255),
    (20, 131, 212, 255),
    (20, 132, 211, 255),
    (20, 133, 211, 255),
    (19, 135, 211, 255),
    (19, 136, 210, 255),
    (19, 137, 210, 255),
    (18, 138, 210, 255),
    (17, 139, 210, 255),
    (17, 140, 210, 255),
    (16, 142, 210, 255),
    (15, 143, 210, 255),
    (14, 144, 209, 255),
    (13, 146, 209, 255),
    (12, 147, 209, 255),
    (11, 148, 209, 255),
    (10, 149, 209, 255),
    (9, 151, 209, 255),
    (8, 152, 209, 255),
    (8, 153, 208, 255),
    (7, 154, 208, 255),
    (7, 155, 207, 255),
    (6, 156, 207, 255),
    (6, 157, 206, 255),
    (6, 158, 206, 255),
    (6, 159, 205, 255),
    (6, 160, 204, 255),
    (6, 161, 204, 255),
    (5, 161, 203, 255),
    (5, 162, 202, 255),
    (5, 163, 201, 255),
    (5, 164, 200, 255),
    (5, 165, 200, 255),
    (5, 165, 199, 255),
    (5, 166, 198, 255),
    (5, 167, 197, 255),
    (6, 167, 196, 255),
    (6, 168, 195, 255),
    (6, 169, 194, 255),
    (7, 169, 193, 255),
    (7, 170, 192, 255),
    (8, 171, 190, 255),
    (9, 171, 189, 255),
    (10, 172, 188, 255),
    (11, 172, 187, 255),
    (13, 173, 186, 255),
    (14, 174, 185, 255),
    (16, 174, 184, 255),
    (17, 175, 182, 255),
    (19, 175, 181, 255),
    (20, 176, 180, 255),
    (22, 177, 179, 255),
    (24, 177, 177, 255),
    (26, 178, 176, 255),
    (28, 178, 175, 255),
    (30, 179, 174, 255),
    (32, 179, 172, 255),
    (34, 180, 171, 255),
    (36, 180, 170, 255),
    (38, 181, 168, 255),
    (40, 181, 167, 255),
    (42, 182, 165, 255),
    (44, 182, 164, 255),
    (47, 183, 163, 255),
    (49, 183, 161, 255),
    (51, 184, 160, 255),
    (54, 184, 158, 255),
    (56, 185, 157, 255),
    (59, 185, 155, 255),
    (61, 185, 154, 255),
    (64, 186, 152, 255),
    (67, 186, 151, 255),
    (69, 187, 149, 255),
    (72, 187, 148, 255),
    (75, 187, 146, 255),
    (78, 188, 145, 255),
    (81, 188, 143, 255),
    (83, 188, 142, 255),
    (86, 189, 140, 255),
    (89, 189, 139, 255),
    (92, 189, 137, 255),
    (95, 189, 136, 255),
    (98, 190, 134, 255),
    (101, 190, 133, 255),
    (104, 190, 131, 255),
    (107, 190, 130, 255),
    (110, 190, 129, 255),
    (113, 190, 128, 255),
    (116, 190, 126, 255),
    (119, 190, 125, 255),
    (121, 190, 124, 255),
    (124, 191, 123, 255),
    (127, 191, 122, 255),
    (130, 191, 120, 255),
    (132, 191, 119, 255),
    (135, 191, 118, 255),
    (138, 190, 117, 255),
    (140, 190, 116, 255),
    (143, 190, 115, 255),
    (145, 190, 114, 255),
    (148, 190, 113, 255),
    (150, 190, 112, 255),
    (153, 190, 111, 255),
    (155, 190, 110, 255),
    (158, 190, 109, 255),
    (160, 190, 108, 255),
    (162, 190, 107, 255),
    (165, 190, 106, 255),
    (167, 190, 105, 255),
    (169, 189, 104, 255),
    (171, 189, 104, 255),
    (174, 189, 103, 255),
    (176, 189, 102, 255),
    (178, 189, 101, 255),
    (180, 189, 100, 255),
    (182, 189, 99, 255),
    (185, 188, 98, 255),
    (187, 188, 97, 255),
    (189, 188, 97, 255),
    (191, 188, 96, 255),
    (193, 188, 95, 255),
    (195, 187, 94, 255),
    (197, 187, 93, 255),
    (199, 187, 92, 255),
    (202, 187, 91, 255),
    (204, 187, 91, 255),
    (206, 187, 90, 255),
    (208, 186, 89, 255),
    (210, 186, 88, 255),
    (212, 186, 87, 255),
    (214, 186, 86, 255),
    (216, 186, 85, 255),
    (218, 185, 85, 255),
    (220, 185, 84, 255),
    (222, 185, 83, 255),
    (224, 185, 82, 255),
    (226, 185, 81, 255),
    (228, 185, 80, 255),
    (230, 185, 79, 255),
    (232, 185, 78, 255),
    (234, 185, 77, 255),
    (236, 185, 76, 255),
    (238, 185, 75, 255),
    (240, 185, 74, 255),
    (242, 185, 72, 255),
    (243, 185, 71, 255),
    (245, 185, 70, 255),
    (247, 186, 68, 255),
    (249, 186, 67, 255),
    (250, 187, 65, 255),
    (251, 188, 63, 255),
    (253, 189, 62, 255),
    (253, 190, 60, 255),
    (254, 191, 58, 255),
    (254, 193, 57, 255),
    (254, 194, 55, 255),
    (254, 195, 54, 255),
    (254, 197, 53, 255),
    (254, 198, 52, 255),
    (254, 199, 50, 255),
    (253, 200, 49, 255),
    (253, 202, 48, 255),
    (252, 203, 47, 255),
    (252, 204, 46, 255),
    (251, 206, 45, 255),
    (251, 207, 44, 255),
    (250, 208, 43, 255),
    (250, 209, 42, 255),
    (249, 211, 41, 255),
    (248, 212, 40, 255),
    (248, 213, 39, 255),
    (247, 215, 38, 255),
    (247, 216, 37, 255),
    (246, 217, 36, 255),
    (246, 219, 35, 255),
    (245, 220, 34, 255),
    (245, 222, 33, 255),
    (245, 223, 32, 255),
    (244, 225, 30, 255),
    (244, 226, 29, 255),
    (244, 228, 28, 255),
    (244, 230, 27, 255),
    (244, 231, 26, 255),
    (244, 233, 25, 255),
    (244, 235, 24, 255),
    (245, 237, 22, 255),
    (245, 238, 21, 255),
    (245, 240, 20, 255),
    (246, 242, 19, 255),
    (246, 244, 17, 255),
    (247, 246, 16, 255),
    (248, 248, 15, 255),
    (248, 250, 13, 255)] 

    return(parula)

#parula = mpl.colors.ListedColormap(name='parula', colors=np.divide(parula, 255.), N=len(parula))
#register_cmap(cmap=parula)
