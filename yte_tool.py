"""
Tool Y Tế - Được train từ dữ liệu OK-2.csv
Tool chuyên biệt để phân tích dữ liệu bệnh nhân sỏi thận PCNL
"""

import pandas as pd
import os
from typing import Dict, List, Any, Optional

# Load dữ liệu trực tiếp từ OK-2.csv
def load_yte_data():
    """Load dữ liệu y tế trực tiếp từ OK-2.csv"""
    try:
        if os.path.exists('OK-2.csv'):
            # Đọc CSV với pandas, xử lý decimal separator
            df = pd.read_csv('OK-2.csv', decimal=',')
            
            # Chuyển đổi DataFrame thành list of dict
            patients = []
            for index, row in df.iterrows():
                # Tính tuổi từ năm sinh
                birth_year = safe_convert(row.get('Năm sinh ', row.get('Năm sinh')))
                age = 2025 - birth_year if birth_year else None
                
                patient = {
                    'id': index + 1,
                    'birth_year': birth_year,
                    'age': age,
                    'gender': str(row.get('Giới tính', '')).strip(),
                    'admission_date': str(row.get('Ngày nhập viện ', row.get('Ngày nhập viện', ''))).strip(),
                    'height': safe_convert(row.get('Chiều cao', '')),
                    'weight': safe_convert(row.get('Cân nặng ', row.get('Cân nặng', ''))),
                    'bmi': safe_convert(row.get('BMI', '')),
                    'medical_history': str(row.get('Tiền căn nội khoa ', row.get('Tiền căn nội khoa', ''))).strip(),
                    'previous_surgery': str(row.get('Tiền căn đã mổ sỏi thận ', row.get('Tiền căn đã mổ sỏi thận', ''))).strip(),
                    'stone_type': str(row.get('Loại sỏi ', row.get('Loại sỏi', ''))).strip(),
                    'stone_size': str(row.get('Kích thước sỏi 3 chiều (khối lớn nhất) ', row.get('Kích thước sỏi 3 chiều (khối lớn nhất)', ''))).strip(),
                    'num_stones': safe_convert(row.get('Số lượng sỏi ', row.get('Số lượng sỏi', ''))),
                    'hu': safe_convert(row.get('HU', '')),
                    'surgery_date': str(row.get('Ngày PT', '')).strip(),
                    'surgery_position': str(row.get('Tư thế', '')).strip(),
                    'surgery_time_minutes': safe_convert(row.get('Thời gian phẫu thuật (phút)', '')),
                    'surgery_result': str(row.get('Sạch sỏi trên C-arm ngay sau mổ ', row.get('Sạch sỏi trên C-arm ngay sau mổ', ''))).strip(),
                    'residual_stones': str(row.get('Nếu sót sỏi trên C-arm ngay sau mổ (số lượng/vị trí/kích thước) ', '')).strip(),
                    'complications': str(row.get('Biến chứng ', row.get('Biến chứng', ''))).strip(),
                    'hb': safe_convert(row.get('Hb (g/dL)', '')),
                    'plt': safe_convert(row.get('PLT (K/uL)', '')),
                    'creatinin': safe_convert(row.get('Creatinin ', row.get('Creatinin', ''))),
                    'egfr': safe_convert(row.get('eGFR', '')),
                }
                
                # Tính BMI nếu có chiều cao và cân nặng và chưa có BMI
                if not patient['bmi'] and patient['height'] and patient['weight']:
                    height_m = patient['height'] / 100
                    patient['bmi'] = round(patient['weight'] / (height_m ** 2), 1)
                
                patients.append(patient)
            
            print(f"✅ Đã load {len(patients)} bệnh nhân từ OK-2.csv")
            return patients
            
        else:
            print("⚠️ Không tìm thấy file OK-2.csv")
            return []
            
    except Exception as e:
        print(f"❌ Lỗi đọc file OK-2.csv: {e}")
        return []

def safe_convert(value):
    """Chuyển đổi an toàn giá trị sang số"""
    if pd.isna(value) or value == '' or value is None:
        return None
    try:
        # Xử lý decimal comma
        if isinstance(value, str):
            value = value.replace(',', '.')
        return float(value)
    except:
        return None

# Dữ liệu y tế load trực tiếp từ CSV
YTE_DATA = load_yte_data()

def yte(query: str) -> str:
    """
    Tool Y Tế - Phân tích dữ liệu bệnh nhân sỏi thận từ OK-2.csv
    
    Args:
        query (str): Câu hỏi phân tích y tế
        
    Returns:
        str: Kết quả phân tích dữ liệu y tế
    """
    print(f"\n🏥 YTE Tool Call: yte(query='{query}')")
    
    if not YTE_DATA:
        return "❌ Không có dữ liệu y tế để phân tích"
    
    query_lower = query.lower()
    total_patients = len(YTE_DATA)
    
    # Phân tích tổng quan
    if any(keyword in query_lower for keyword in ["tổng quan", "overview", "thống kê", "tong quan"]):
        male_count = sum(1 for p in YTE_DATA if p.get("gender") == "Nam")
        female_count = sum(1 for p in YTE_DATA if p.get("gender") == "Nữ")
        
        ages = [p.get("age") for p in YTE_DATA if p.get("age") is not None]
        avg_age = sum(ages) / len(ages) if ages else 0
        
        # Phân tích kết quả phẫu thuật
        sach_soi = sum(1 for p in YTE_DATA if "Có" in str(p.get("surgery_result", "")))
        sot_soi = sum(1 for p in YTE_DATA if "Sót" in str(p.get("surgery_result", "")))
        
        # Tính tỷ lệ Nam/Nữ an toàn
        ratio_text = f"{male_count/female_count:.1f}:1" if female_count > 0 else f"{male_count}:0"
        
        result = f"""🏥 THỐNG KÊ TỔNG QUAN Y TẾ (Dữ liệu OK-2.csv)

📊 TỔNG SỐ BỆNH NHÂN: {total_patients}

👫 PHÂN BỐ GIỚI TÍNH:
▪️ Nam: {male_count} bệnh nhân ({male_count/total_patients*100:.1f}%)
▪️ Nữ: {female_count} bệnh nhân ({female_count/total_patients*100:.1f}%)
▪️ Tỷ lệ Nam/Nữ: {ratio_text}

📈 THÔNG TIN TUỔI:
▪️ Tuổi trung bình: {avg_age:.1f} tuổi"""
        
        if ages:
            result += f"""
▪️ Tuổi thấp nhất: {min(ages)} tuổi
▪️ Tuổi cao nhất: {max(ages)} tuổi"""
        
        result += f"""

🎯 KẾT QUẢ PHẪU THUẬT PCNL:
▪️ Sạch sỏi: {sach_soi} ca ({sach_soi/total_patients*100:.1f}%)
▪️ Sót sỏi: {sot_soi} ca ({sot_soi/total_patients*100:.1f}%)

📅 Dữ liệu: Train từ OK-2.csv - {total_patients} bệnh nhân sỏi thận PCNL"""
        
        return result
    
    # Phân tích giới tính
    elif any(keyword in query_lower for keyword in ["giới tính", "gender", "nam nữ", "gioi tinh"]):
        male_patients = [p for p in YTE_DATA if p.get("gender") == "Nam"]
        female_patients = [p for p in YTE_DATA if p.get("gender") == "Nữ"]
        
        male_ages = [p.get("age") for p in male_patients if p.get("age") is not None]
        female_ages = [p.get("age") for p in female_patients if p.get("age") is not None]
        
        male_avg = sum(male_ages) / len(male_ages) if male_ages else 0
        female_avg = sum(female_ages) / len(female_ages) if female_ages else 0
        
        # Tính tỷ lệ Nam/Nữ an toàn
        gender_ratio = f"{len(male_patients)/len(female_patients):.1f}:1" if len(female_patients) > 0 else f"{len(male_patients)}:0"
        
        result = f"""👫 PHÂN TÍCH GIỚI TÍNH (Dữ liệu OK-2.csv)

👨 NAM GIỚI: {len(male_patients)} bệnh nhân
▪️ Tuổi trung bình: {male_avg:.1f} tuổi
▪️ ID bệnh nhân: {[p.get("id") for p in male_patients]}
▪️ Chiếm tỷ lệ: {len(male_patients)/total_patients*100:.1f}%

👩 NỮ GIỚI: {len(female_patients)} bệnh nhân
▪️ Tuổi trung bình: {female_avg:.1f} tuổi  
▪️ ID bệnh nhân: {[p.get("id") for p in female_patients]}
▪️ Chiếm tỷ lệ: {len(female_patients)/total_patients*100:.1f}%

📊 SO SÁNH:
▪️ Tỷ lệ Nam/Nữ: {gender_ratio}
▪️ Chênh lệch tuổi TB: {abs(male_avg - female_avg):.1f} tuổi"""
        
        return result
    
    # Phân tích sỏi
    elif any(keyword in query_lower for keyword in ["sỏi", "stone", "loại sỏi", "soi"]):
        stone_types = {}
        for patient in YTE_DATA:
            stone_type = patient.get('stone_type', 'Không xác định')
            if stone_type and stone_type != 'Không xác định':
                stone_types[stone_type] = stone_types.get(stone_type, 0) + 1
        
        result = f"""🪨 PHÂN TÍCH LOẠI SỎI (Dữ liệu OK-2.csv)

📊 PHÂN LOẠI SỎI THẬN:"""
        
        for stone_type, count in sorted(stone_types.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_patients) * 100
            result += f"\n▪️ {stone_type}: {count} ca ({percentage:.1f}%)"
        
        most_common = max(stone_types.items(), key=lambda x: x[1]) if stone_types else ("N/A", 0)
        
        result += f"""\n\n📈 THỐNG KÊ SỎI:
▪️ Tổng số loại: {len(stone_types)} loại khác nhau
▪️ Phổ biến nhất: {most_common[0]} ({most_common[1]} ca)
▪️ Đa dạng: {len(stone_types)/total_patients*100:.1f}% tỷ lệ đa dạng loại sỏi"""
        
        return result
    
    # Chi tiết bệnh nhân theo ID
    elif any(keyword in query_lower for keyword in ["bệnh nhân", "patient", "id", "benh nhan"]):
        # Tìm ID trong query
        import re
        id_match = re.search(r'\b(\d+)\b', query)
        
        if id_match:
            patient_id = int(id_match.group(1))
            patient = next((p for p in YTE_DATA if p.get("id") == patient_id), None)
            
            if patient:
                result = f"""👤 CHI TIẾT BỆNH NHÂN ID {patient_id} (OK-2.csv)

🏷️ THÔNG TIN CÁ NHÂN:
▪️ Tuổi: {patient.get('age', 'N/A')} tuổi ({patient.get('birth_year', 'N/A')})
▪️ Giới tính: {patient.get('gender', 'N/A')}
▪️ Ngày nhập viện: {patient.get('admission_date', 'N/A')}
▪️ Chiều cao: {patient.get('height', 'N/A')} cm
▪️ Cân nặng: {patient.get('weight', 'N/A')} kg
▪️ BMI: {patient.get('bmi', 'N/A')}

🏥 TIỀN CĂN BỆNH LÝ:
▪️ Bệnh lý nội khoa: {patient.get('medical_history', 'Không có')}
▪️ Tiền sử PT sỏi: {patient.get('previous_surgery', 'Chưa mổ') if patient.get('previous_surgery') else 'Chưa mổ'}

🪨 THÔNG TIN SỎI:
▪️ Loại sỏi: {patient.get('stone_type', 'N/A')}
▪️ Kích thước: {patient.get('stone_size', 'N/A')}
▪️ Mật độ HU: {patient.get('hu', 'N/A')}
▪️ Số lượng: {patient.get('num_stones', 'N/A')}

⚕️ PHẪU THUẬT PCNL:
▪️ Ngày PT: {patient.get('surgery_date', 'N/A')}
▪️ Tư thế: {patient.get('surgery_position', 'N/A')}
▪️ Thời gian PT: {patient.get('surgery_time_minutes', 'N/A')} phút
▪️ Kết quả: {patient.get('surgery_result', 'N/A')}
▪️ Sỏi còn lại: {patient.get('residual_stones', 'Không') if patient.get('residual_stones') else 'Không'}
▪️ Biến chứng: {patient.get('complications', 'Không') if patient.get('complications') else 'Không'}

🔬 XÉT NGHIỆM:
▪️ Hb: {patient.get('hb', 'N/A')} g/dL
▪️ PLT: {patient.get('plt', 'N/A')} K/uL  
▪️ Creatinin: {patient.get('creatinin', 'N/A')} μmol/L
▪️ eGFR: {patient.get('egfr', 'N/A')} mL/min"""
                
                return result
            else:
                available_ids = [p.get("id") for p in YTE_DATA]
                return f"❌ Không tìm thấy bệnh nhân ID {patient_id}\n📋 ID có sẵn: {available_ids}"
        else:
            # Liệt kê tất cả bệnh nhân
            result = f"""👥 DANH SÁCH BỆNH NHÂN (OK-2.csv)

📋 {total_patients} BỆNH NHÂN SỎI THẬN PCNL:"""
            
            for patient in YTE_DATA:
                result += f"\n▪️ ID {patient.get('id')}: {patient.get('gender')} {patient.get('age')} tuổi - {patient.get('stone_type', 'N/A')}"
                
            return result
    
    # Phân tích phẫu thuật
    elif any(keyword in query_lower for keyword in ["phẫu thuật", "pt", "surgery", "phau thuat"]):
        surgery_results = {}
        surgery_times = []
        complications = []
        
        for patient in YTE_DATA:
            # Kết quả PT
            result = patient.get('surgery_result', 'Không xác định')
            surgery_results[result] = surgery_results.get(result, 0) + 1
            
            # Thời gian PT
            if patient.get('surgery_time_minutes'):
                surgery_times.append(patient.get('surgery_time_minutes'))
            
            # Biến chứng
            if patient.get('complications'):
                complications.append(patient.get('complications'))
        
        avg_time = sum(surgery_times) / len(surgery_times) if surgery_times else 0
        
        result = f"""⚕️ PHÂN TÍCH PHẪU THUẬT PCNL (OK-2.csv)

🎯 KẾT QUẢ PHẪU THUẬT:"""
        
        for surg_result, count in surgery_results.items():
            percentage = (count / total_patients) * 100
            result += f"\n▪️ {surg_result}: {count} ca ({percentage:.1f}%)"
        
        result += f"""\n\n⏱️ THỜI GIAN PHẪU THUẬT:
▪️ Thời gian TB: {avg_time:.1f} phút
▪️ Thời gian ngắn nhất: {min(surgery_times) if surgery_times else 'N/A'} phút
▪️ Thời gian dài nhất: {max(surgery_times) if surgery_times else 'N/A'} phút

🚨 BIẾN CHỨNG:
▪️ Có biến chứng: {len([c for c in complications if c])} ca
▪️ Không biến chứng: {total_patients - len([c for c in complications if c])} ca
▪️ Tỷ lệ an toàn: {((total_patients - len([c for c in complications if c]))/total_patients*100):.1f}%"""
        
        return result
    
    # BMI analysis
    elif any(keyword in query_lower for keyword in ["bmi", "cân nặng", "béo phì", "can nang"]):
        bmis = []
        heights = []
        weights = []
        
        for patient in YTE_DATA:
            if patient.get('height') and patient.get('weight'):
                height_m = patient.get('height') / 100
                weight_kg = patient.get('weight')
                bmi = weight_kg / (height_m ** 2)
                bmis.append(bmi)
                heights.append(patient.get('height'))
                weights.append(patient.get('weight'))
        
        if bmis:
            avg_bmi = sum(bmis) / len(bmis)
            avg_height = sum(heights) / len(heights)
            avg_weight = sum(weights) / len(weights)
            
            # Phân loại BMI
            underweight = len([b for b in bmis if b < 18.5])
            normal = len([b for b in bmis if 18.5 <= b < 25])
            overweight = len([b for b in bmis if 25 <= b < 30])
            obese = len([b for b in bmis if b >= 30])
            
            result = f"""⚖️ PHÂN TÍCH BMI VÀ CÂN NẶNG (OK-2.csv)

📊 THỐNG KÊ CHUNG:
▪️ BMI trung bình: {avg_bmi:.1f}
▪️ Chiều cao TB: {avg_height:.1f} cm
▪️ Cân nặng TB: {avg_weight:.1f} kg

📈 PHÂN LOẠI BMI (WHO):
▪️ Thiếu cân (<18.5): {underweight} ca ({underweight/len(bmis)*100:.1f}%)
▪️ Bình thường (18.5-24.9): {normal} ca ({normal/len(bmis)*100:.1f}%)
▪️ Thừa cân (25-29.9): {overweight} ca ({overweight/len(bmis)*100:.1f}%)
▪️ Béo phì (≥30): {obese} ca ({obese/len(bmis)*100:.1f}%)

💡 NHẬN XÉT:
▪️ Phần lớn bệnh nhân có BMI: {"Bình thường" if normal == max(underweight, normal, overweight, obese) else "Thừa cân" if overweight == max(underweight, normal, overweight, obese) else "Béo phì" if obese == max(underweight, normal, overweight, obese) else "Thiếu cân"}
▪️ Tỷ lệ thừa cân + béo phì: {(overweight + obese)/len(bmis)*100:.1f}%"""
            
            return result
        else:
            return "❌ Không có đủ dữ liệu chiều cao/cân nặng để tính BMI"
    
    # Tìm kiếm chung
    else:
        result = f"""🔍 TÌM KIẾM Y TẾ: "{query}"

📊 DỮ LIỆU CÓ SẴN (OK-2.csv):
▪️ {total_patients} bệnh nhân sỏi thận PCNL
▪️ 107 cột dữ liệu chi tiết
▪️ Thông tin phẫu thuật đầy đủ

💡 CÁC LOẠI PHÂN TÍCH:
▪️ "tổng quan" - Thống kê tổng quát
▪️ "giới tính" - Phân bố nam/nữ
▪️ "sỏi" - Phân tích loại sỏi
▪️ "bệnh nhân [ID]" - Chi tiết bệnh nhân
▪️ "phẫu thuật" - Kết quả PT PCNL
▪️ "bmi" - Phân tích cân nặng

🏥 VÍ DỤ TRUY VẤN:
▪️ yte("tổng quan bệnh nhân")
▪️ yte("phân tích giới tính")
▪️ yte("bệnh nhân ID 1")
▪️ yte("loại sỏi phổ biến")"""
        
        return result

def yte_info() -> str:
    """Thông tin về tool y tế"""
    return f"""🏥 YTE TOOL - PHÂN TÍCH Y TẾ

📊 DỮ LIỆU:
▪️ Nguồn: OK-2.csv
▪️ Số bệnh nhân: {len(YTE_DATA)}
▪️ Loại bệnh: Sỏi thận PCNL
▪️ Cột dữ liệu: 107 cột

🔧 CHỨC NĂNG:
▪️ Thống kê tổng quan
▪️ Phân tích giới tính & tuổi
▪️ Phân loại sỏi thận
▪️ Chi tiết bệnh nhân
▪️ Kết quả phẫu thuật
▪️ Phân tích BMI

🎯 CÁCH SỬ DỤNG:
yte("câu hỏi phân tích y tế")

💡 Tool chuyên biệt cho phân tích dữ liệu y tế từ OK-2.csv"""

if __name__ == "__main__":
    print(yte_info())
    print("\n" + "="*50)
    print("🧪 Test YTE Tool:")
    print(yte("tổng quan bệnh nhân"))
