import carla

def locate_vehicle():
    try:
        # 连接到服务器
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()

        # 查找所有车辆
        vehicles = world.get_actors().filter('vehicle.*')

        if not vehicles:
            print("❌ 未找到任何车辆！请确认 manual_control.py 正在运行。")
            return

        print(f"✅ 找到了 {len(vehicles)} 辆车。正在标记...")

        for v in vehicles:
            loc = v.get_location()
            # 1. 打印坐标
            print(f" -> 车辆: {v.type_id} | ID: {v.id}")
            print(f"    位置: X={loc.x:.1f}, Y={loc.y:.1f}, Z={loc.z:.1f}")
            
            # 2. 在 UE4 屏幕里画一个巨大的红色方框 (长宽高 4米x4米x10米)
            # 这样就算隔着楼房你也能看到那条红线
            world.debug.draw_box(
                carla.BoundingBox(v.get_transform().location, carla.Vector3D(2,2,5)),
                v.get_transform().rotation,
                0.5,  # 线条粗细
                carla.Color(255, 0, 0, 0), # 红色
                60.0) # 持续显示 60 秒
            
            # 3. 在车辆头顶写字
            world.debug.draw_string(
                v.get_location() + carla.Location(z=2), 
                "HERE IS YOUR BIKE!", 
                draw_shadow=False,
                color=carla.Color(255, 0, 0, 0), 
                life_time=60.0)

        print("\n🚀 请现在回到 UE4 编辑器视口，寻找【红色的方框】！")
        print("💡 提示：你可以根据上方打印的 X,Y 坐标，在编辑器里看左上角的小地图或坐标轴飞行。")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    locate_vehicle()