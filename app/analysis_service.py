from app.model_analysis import AnalysisData


class AnalysisService:
    @staticmethod
    def perform_analysis():
        results = []
        try:
            # 获取数据
            raw_data = AnalysisData.get_analysis_data()

            if not raw_data:  # 添加空数据检查
                print("警告: 获取到的数据为空")
                return 0

            for row in raw_data:
                star = 0  # 每次循环重置
                company_id = row.get("company_id")
                room_count = row.get("room_count", 0) or 0  # 处理可能的None
                regi_count = row.get("regi_roomCount", 0) or 0
                companyType = row.get("companyType")

                if room_count >= regi_count and room_count >= 30:
                    star = 5
                elif regi_count > room_count and regi_count >= 30:
                    star = 4
                elif companyType=="homestay" and ((room_count>=10 and room_count < 30) or (regi_count>=10 and regi_count<30)):
                    star= 3
                elif (companyType == "hotel" or companyType == "youthHostel") and ((room_count>=10 and room_count < 30) or (regi_count >= 10 and regi_count < 30)):
                    star= 3

                if company_id:  # 确保company_id存在
                    results.append({"company_id": company_id, "star": star})

            if not results:  # 添加结果空检查
                print("警告: 没有符合条件的数据")
                return 0

            updated_rows = AnalysisData.save_data(results)
            print(f"成功更新 {updated_rows} 条数据")
            return updated_rows

        except Exception as e:
            print(f"分析失败: {str(e)}")
            # 不再使用空的 raise，而是返回错误代码
            return 0
